# Implementación Postgres + pgvector

Guía de cómo se agregó persistencia Postgres (con pgvector) a este proyecto
**sin acoplar la base de datos al funcionamiento de la API**. El diseño sigue
la arquitectura hexagonal que ya tenía el repo: la DB es un *adaptador* más,
intercambiable con el de memoria mediante una variable de entorno.

Patrón tomado de `marvik/deepflow-monorepo` (`backend/app/core/db.py`,
`domains/commercial_slides_rag/models.py`), adaptado a **sync** porque el
puerto `IReviewRepository` del curso es sincrónico.

---

## 1. Idea: desacoplamiento por puerto

El dominio define un **puerto** (interfaz). Las implementaciones concretas son
**adaptadores** que la API elige en runtime. Ni los casos de uso ni el dominio
saben si hay Postgres detrás.

```
        ┌─────────────────────────────────────────────┐
        │              Casos de uso (app)              │
        │   SendReview / GetReview / ListReviews ...   │
        └───────────────────┬─────────────────────────┘
                            │  depende de
                            ▼
              src/domain/ports/review_repository.py
                    IReviewRepository (ABC)
              save / find_by_pr_id / find_by_id /
                      find_all / delete
                            ▲
            ┌───────────────┴───────────────┐
   implementa │                              │ implementa
            │                              │
 InMemoryReviewRepository          DBReviewRepository
 (dict en memoria)                 (Postgres + pgvector)
```

El switch vive en `src/infrastructure/api/http_api.py` → `_build_repository()`,
que mira `REPOSITORY_BACKEND` (`memory` por default, `db`/`postgres` para Postgres).

---

## 2. Archivos nuevos / modificados

| Archivo | Rol |
|---|---|
| `src/infrastructure/persistence/config.py` | **Nuevo.** Settings de DB (`DatabaseSettings`, pydantic-settings) + `database_url`. |
| `src/infrastructure/persistence/database.py` | **Nuevo.** `create_db_engine`, `create_session_factory`, `run_migrations` (alembic upgrade head), `init_db` (helper para tests), `close_db`. |
| `src/infrastructure/persistence/models.py` | **Nuevo.** `ReviewModel` (SQLModel) con columna `embedding` pgvector + mapeo dominio↔fila. |
| `src/infrastructure/persistence/db_repository.py` | **Reescrito.** `DBReviewRepository` real (antes era un placeholder = copia del in-memory). |
| `alembic.ini`, `migrations/` | **Nuevo.** Alembic + migración inicial `0001_initial`. |
| `src/infrastructure/api/http_api.py` | `_build_repository()` con el switch memory/db (default **db**). |
| `pyproject.toml` | + `sqlmodel`, `psycopg[binary]`, `pgvector`, `pydantic-settings`, `alembic`. |
| `Dockerfile` | Copia `alembic.ini` + `migrations/` al runtime. |
| `docker-compose.yml` | Servicio `db` con imagen `pgvector/pgvector:pg16` + volumen + healthcheck. |
| `.env.example` | Variables `REPOSITORY_BACKEND`, `POSTGRES_*`, `EMBEDDING_DIMENSIONS`. |

> El dominio (`src/domain/`) **no cambió**. SQLModel/pgvector solo aparecen
> dentro de `infrastructure/persistence`. Eso es el desacoplamiento.

---

## 3. El modelo (pgvector)

`ReviewModel` es el espejo persistente de la entidad `Review`. La columna
`embedding` es `Vector(n)` (n configurable, default 1536) y **nullable**: el
dominio no la conoce, habilita búsqueda semántica sin contaminar la entidad.

```python
class ReviewModel(SQLModel, table=True):
    __tablename__ = "reviews"
    id: str = Field(primary_key=True)
    pr_id: str = Field(index=True)
    status: str = Field(default=ReviewStatus.PENDING.value)
    rating: int | None = None
    summary: str = ""
    recommendations: list[str] = Field(sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(sa_type=DateTime(timezone=True))
    completed_at: datetime | None = Field(sa_type=DateTime(timezone=True))
    embedding: Any = Field(sa_column=Column(Vector(_EMBEDDING_DIM), nullable=True))
```

El mapeo dominio↔persistencia se hace con `from_domain` / `apply_domain` /
`to_domain` en el propio modelo. `apply_domain` **no toca `embedding`**: lo
gestiona quien indexe, no el flujo de reviews.

---

## 4. Migraciones (Alembic)

El esquema lo gestiona **Alembic** (fuente de verdad única). La migración inicial
`migrations/versions/0001_initial.py` habilita pgvector, crea la tabla `reviews`
y el índice HNSW para similitud coseno:

```python
def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")  # antes de la columna Vector
    op.create_table("reviews", ... , sa.Column("embedding", Vector(_EMBEDDING_DIM)))
    op.create_index("ix_reviews_pr_id", "reviews", ["pr_id"])
    op.execute(
        "CREATE INDEX IF NOT EXISTS reviews_embedding_hnsw "
        "ON reviews USING hnsw (embedding vector_cosine_ops)"
    )
```

Archivos:

| Archivo | Rol |
|---|---|
| `alembic.ini` | Config; `script_location = migrations`. La URL **no** vive acá. |
| `migrations/env.py` | Toma la URL de `DatabaseSettings`, `target_metadata = SQLModel.metadata`. |
| `migrations/versions/0001_initial.py` | Migración inicial (extensión + tabla + índices). |

### Cuándo se ejecuta

`run_migrations()` (en `database.py`) corre `alembic upgrade head` al **arrancar
la app con backend de Postgres** (lo llama `_build_repository`). Es idempotente:
si la DB ya está en `head`, no hace nada. Esto cubre todos los entrypoints
(`fastapi dev`, `fastapi run`, Docker) sin pasos manuales.

```python
def run_migrations() -> None:
    cfg = Config(str(_REPO_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(_REPO_ROOT / "migrations"))
    command.upgrade(cfg, "head")
```

A mano (opcional):

```bash
alembic upgrade head          # aplicar
alembic downgrade -1          # revertir la última
alembic revision -m "msg"     # crear una nueva migración
```

> `init_db()` (CREATE EXTENSION + `create_all` + índice, inline) queda como helper
> para tests rápidos sin Alembic, pero **el path de la app usa migraciones**.

---

## 5. El adaptador (`DBReviewRepository`)

Cumple `IReviewRepository` (mismo contrato que el in-memory). Cada operación
abre una **sesión corta** (unit of work) y la cierra: la sesión no se acopla al
request de FastAPI, el adaptador queda autocontenido.

- `save` → upsert por `id` (get + create/`apply_domain` + commit).
- `find_by_pr_id` → review más reciente del PR (`order_by created_at desc`).
- `find_by_id`, `find_all`, `delete`, `clear` → directos.
- **Extra (fuera del puerto):** `find_similar(embedding, top_k)` → búsqueda por
  similitud coseno con el operador `<=>` de pgvector vía
  `ReviewModel.embedding.cosine_distance(...)`.

```python
stmt = (
    select(ReviewModel)
    .where(ReviewModel.embedding.is_not(None))
    .order_by(ReviewModel.embedding.cosine_distance(embedding))
    .limit(top_k)
)
```

---

## 6. El switch (intercambiable)

```python
def _build_repository() -> IReviewRepository:
    backend = os.environ.get("REPOSITORY_BACKEND", "db").lower()
    if backend == "memory":
        return InMemoryReviewRepository()
    from src.infrastructure.persistence.database import (
        create_db_engine, create_session_factory, run_migrations)
    from src.infrastructure.persistence.db_repository import DBReviewRepository
    run_migrations()                       # alembic upgrade head (idempotente)
    engine = create_db_engine()
    return DBReviewRepository(create_session_factory(engine))
```

**Default = `db`**: el código usa Postgres salvo que se pida `REPOSITORY_BACKEND=memory`
(tests / sin DB). Import **lazy**: en modo memoria no hace falta sqlalchemy/pgvector.
Cambiar de backend = una variable de entorno, sin tocar código.

---

## 7. Cómo usarlo

### Local (solo levantar Postgres con pgvector)

```bash
docker run -d --name curso-ai-db \
  -e POSTGRES_USER=app -e POSTGRES_PASSWORD=changethis -e POSTGRES_DB=curso_ai \
  -p 5432:5432 pgvector/pgvector:pg16

# .env
REPOSITORY_BACKEND=db
POSTGRES_HOST=localhost
POSTGRES_USER=app
POSTGRES_PASSWORD=changethis
POSTGRES_DB=curso_ai

uv pip install -e .
fastapi dev
```

### Docker Compose (todo junto)

```bash
REPOSITORY_BACKEND=db docker compose up --build
```

El servicio `backend` apunta a `POSTGRES_HOST=db` (nombre del servicio en la red
de compose) y espera el healthcheck de la DB antes de arrancar.

### Volver a memoria

```bash
REPOSITORY_BACKEND=memory   # o borrar la variable
```

---

## 8. Verificación

Probado end-to-end contra `pgvector/pgvector:pg16`:

- CRUD completo (`save` upsert, `find_by_pr_id`, `find_by_id`, `find_all`, `delete`).
- `init_db` crea extensión + tabla + índice HNSW.
- `find_similar` ordena por cercanía coseno correctamente.

```python
sim = repo.find_similar([0.9, 0.1, 0, 0], top_k=2)
# -> el review con embedding [1,0,0,0] queda primero
```

---

## 9. Próximos pasos (opcionales)

- **Adaptador de embeddings** (`IEmbedder`) que pueble `embedding` desde el
  `summary` del review → habilita "reviews similares" reales en la API.
- Pasar el stack a **async** (`create_async_engine` + `asyncpg`) si la API migra
  a endpoints async; el puerto pasaría a métodos `async def`.
