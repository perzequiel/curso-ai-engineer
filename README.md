# Curso AI Engineer - Code Review System

Sistema de revision de codigo automatizado con IA, implementado con arquitectura **Ports & Adapters** (Hexagonal Architecture).

## Descripcion

Este proyecto es la base practica para un curso de AI Engineer. Implementa un sistema que:

1. Recibe Pull Requests de GitHub para revision
2. Analiza el codigo usando un agente de IA (LangChain + Claude)
3. Genera una calificacion (0-100) y recomendaciones
4. Aprueba o rechaza segun el umbral (rating > 70)

## Arquitectura

El proyecto sigue **Ports & Adapters** (Hexagonal Architecture), separando claramente:

- **Dominio**: Logica de negocio pura, sin dependencias externas
- **Puertos**: Interfaces abstractas que definen contratos
- **Adaptadores**: Implementaciones concretas (GitHub API, IA, base de datos)

```
Usuario -> Task -> ReviewProcess -> CodeManager -> CodeReviewer (IA)
                                       |                |
                                  GitHub PRCode    rate > 70?
                                       |           /       \
                                      DB         NO        YES
                                              Rejected   Approved
```

## Estructura del Proyecto

```
curso-ai-engineer/
├── curso_AI.md                              # Especificacion completa del curso
├── pyproject.toml                           # Configuracion del proyecto
├── .env.example                             # Variables de entorno de ejemplo
│
├── src/                                     # BACKEND (Python + FastAPI)
│   ├── domain/                              # NUCLEO - Logica de negocio
│   │   ├── entities/
│   │   │   └── review.py                    # Clase 1: Review Entity
│   │   ├── value_objects/
│   │   │   ├── review_status.py             # Enum: PENDING, IN_PROGRESS, COMPLETED, FAILED
│   │   │   └── rating.py                    # Value Object: calificacion 0-100
│   │   └── ports/                           # INTERFACES (Puertos)
│   │       ├── review_repository.py         # Clase 2: IReviewRepository
│   │       ├── code_reviewer.py             # Clase 3: ICodeReviewer
│   │       └── github_client.py             # Clase 4: IGitHubClient
│   │
│   ├── application/                         # Casos de Uso
│   │   └── use_cases/
│   │       ├── send_review.py               # Clase 5: SendReviewUseCase
│   │       ├── get_review_result.py         # Clase 6: GetReviewResultUseCase
│   │       └── list_reviews.py              # Clase 7: ListReviewsUseCase
│   │
│   └── infrastructure/                      # ADAPTADORES
│       ├── persistence/
│       │   └── in_memory_repository.py      # Clase 8: InMemoryReviewRepository
│       ├── github/
│       │   ├── github_adapter.py            # GitHubAdapter (PyGithub)
│       │   └── mock_github_adapter.py       # MockGitHubAdapter (sin deps externas)
│       └── ai/
│           ├── ai_code_reviewer.py          # AICodeReviewer (LangChain + Claude)
│           ├── mock_code_reviewer.py        # MockCodeReviewer (sin deps externas)
│           └── review_rules.py              # Reglas de revision compartidas
│
├── frontend/                                # FRONTEND (Next.js 16 + React 19)
│   ├── app/                                 # App Router de Next.js
│   │   ├── layout.tsx                       # Layout raiz
│   │   ├── page.tsx                         # Dashboard principal (lista de PRs)
│   │   └── globals.css                      # Estilos globales (Tailwind v4)
│   ├── components/
│   │   ├── pr-list.tsx                      # Componente: lista de PRs
│   │   ├── review-detail-dialog.tsx         # Componente: detalle de review
│   │   ├── theme-provider.tsx               # Proveedor de tema (light/dark)
│   │   └── ui/                              # Componentes UI (shadcn/ui + Radix)
│   ├── lib/
│   │   ├── api-service.ts                   # Cliente para la API del backend
│   │   ├── types.ts                         # Tipos compartidos (basados en Swagger)
│   │   ├── mock-data.ts                     # Datos mock para desarrollo
│   │   └── utils.ts                         # Utilidades (cn, etc.)
│   ├── hooks/                               # Custom hooks (use-mobile, use-toast)
│   ├── public/                              # Assets estaticos
│   ├── styles/                              # Estilos adicionales
│   ├── next.config.mjs                      # Configuracion de Next.js
│   ├── tsconfig.json                        # Configuracion de TypeScript
│   └── package.json                         # Dependencias del frontend
│
├── tests/                                   # Tests separados por clase
│   ├── conftest.py                          # Fixtures compartidas
│   ├── clase_1/test_review.py               # Tests Review Entity
│   ├── clase_2/test_review_repository.py    # Tests IReviewRepository
│   ├── clase_3/test_code_reviewer.py        # Tests ICodeReviewer
│   ├── clase_4/test_github_client.py        # Tests IGitHubClient
│   ├── clase_5/test_send_review.py          # Tests SendReviewUseCase
│   ├── clase_6/test_get_review_result.py    # Tests GetReviewResultUseCase
│   ├── clase_7/test_list_reviews.py         # Tests ListReviewsUseCase
│   └── clase_8/test_in_memory_repository.py # Tests InMemoryReviewRepository
│
└── examples/
    └── basic_usage.py                       # Ejemplo de uso completo
```

## Requisitos

- Python 3.11+
- pip o uv (package manager)

## Instalacion

```bash
# Clonar el repositorio
git clone <repo-url>
cd curso-ai-engineer

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -e ".[dev]"

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

## Ejecutar la Aplicacion

La API HTTP esta construida con **FastAPI** y se levanta con el comando `fastapi dev`, que activa hot-reload automatico al cambiar archivos.

```bash
# Levantar el servidor en modo desarrollo (hot-reload)
fastapi dev

# Por defecto queda escuchando en http://127.0.0.1:8000
```

Una vez levantado, tenes disponibles:

- **API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Swagger UI** (docs interactivos): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc** (docs alternativos): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints disponibles


| Metodo | Ruta               | Descripcion                                                                    |
| ------ | ------------------ | ------------------------------------------------------------------------------ |
| `GET`  | `/prs?state=open`  | Lista los PRs del repo configurado en `GITHUB_REPO` (`open`, `closed` o `all`) |
| `POST` | `/reviews`         | Dispara una revision de PR. Body: `{ "pr_id": "<numero>" }`                    |
| `GET`  | `/reviews`         | Lista todas las reviews almacenadas                                            |
| `GET`  | `/reviews/{pr_id}` | Obtiene la review de un PR especifico                                          |


### Ejemplo rapido con `curl`

```bash
# Listar PRs abiertos
curl http://127.0.0.1:8000/prs?state=open

# Disparar una review
curl -X POST http://127.0.0.1:8000/reviews \
  -H "Content-Type: application/json" \
  -d '{"pr_id": "13"}'

# Listar reviews realizadas
curl http://127.0.0.1:8000/reviews
```

### Modo produccion

Para levantar en produccion (sin reload), usa `fastapi run`:

```bash
fastapi run src/infrastructure/api/http_api.py
```

### Variables de entorno requeridas

Si no se setean, la API cae automaticamente a adaptadores **mock**:


| Variable            | Uso                                                                              | Si falta...                                              |
| ------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `GITHUB_TOKEN`      | Token de GitHub para leer PRs                                                    | Se usa `MockGitHubAdapter`                               |
| `GITHUB_REPO`       | Repo en formato `owner/repo`                                                     | Se usa `MockGitHubAdapter`                               |
| `ANTHROPIC_API_KEY` | API key de Claude                                                                | Se usa `MockCodeReviewer`                                |
| `CORS_ORIGINS`      | Origenes permitidos para CORS, separados por coma (ej. `http://localhost:3000`)  | Se permite `http://localhost:3000` y `http://127.0.0.1:3000` |

## Frontend (Next.js)

El proyecto incluye una interfaz web en la carpeta [`frontend/`](frontend/) construida con **Next.js 16** + **React 19** + **TypeScript**, que consume **directamente** la API FastAPI del backend (via `fetch`) para listar Pull Requests y disparar / visualizar revisiones. No usa mocks: todo lo que ves en la UI proviene de los endpoints reales.

### Stack del frontend

| Tecnologia              | Uso                                                  |
| ----------------------- | ---------------------------------------------------- |
| Next.js 16 (App Router) | Framework React con SSR / RSC                        |
| React 19                | Libreria de UI                                       |
| TypeScript 5            | Tipado estatico                                      |
| Tailwind CSS v4         | Estilos utility-first                                |
| shadcn/ui + Radix UI    | Componentes accesibles (dialogs, tabs, tooltip, etc) |
| lucide-react            | Iconos                                               |
| react-hook-form + zod   | Manejo y validacion de formularios                   |
| next-themes             | Soporte de tema claro / oscuro                       |
| sonner                  | Notificaciones (toasts)                              |

### Estructura clave

- `frontend/app/page.tsx`: pagina principal, renderiza el dashboard `<PRList />`.
- `frontend/components/pr-list.tsx`: lista de PRs con filtro de estado y boton para disparar reviews.
- `frontend/components/review-detail-dialog.tsx`: modal con el detalle de la review (rating, summary, recomendaciones).
- `frontend/lib/api-service.ts`: cliente que consume los endpoints del backend (`/prs`, `/reviews`, `/reviews/{pr_id}`).
- `frontend/lib/types.ts`: tipos TypeScript derivados del schema Swagger de la API.

### Requisitos

- Node.js 20+
- npm, pnpm o yarn

### Instalacion y ejecucion

```bash
cd frontend

# Instalar dependencias
npm install
# o, si preferis pnpm (hay pnpm-lock.yaml committeado):
# pnpm install

# (Opcional) Configurar la URL de la API
cp .env.local.example .env.local
# Editar .env.local si la API no corre en http://127.0.0.1:8000

# Levantar el servidor de desarrollo (hot-reload)
npm run dev
# -> http://localhost:3000
```

Para que el frontend pueda llamar al backend, asegurate de tener corriendo la API FastAPI en `http://127.0.0.1:8000` (ver seccion "Ejecutar la Aplicacion" mas arriba). El backend ya viene con **CORS habilitado** para `http://localhost:3000` y `http://127.0.0.1:3000`; si lo levantas en otro host/puerto, configura la variable `CORS_ORIGINS` (ver tabla de variables de entorno).

### Variables de entorno del frontend

| Variable              | Uso                                  | Default                  |
| --------------------- | ------------------------------------ | ------------------------ |
| `NEXT_PUBLIC_API_URL` | URL base de la API FastAPI a llamar  | `http://127.0.0.1:8000`  |

### Scripts disponibles

| Script          | Descripcion                                |
| --------------- | ------------------------------------------ |
| `npm run dev`   | Inicia Next.js en modo desarrollo          |
| `npm run build` | Compila la app para produccion             |
| `npm run start` | Levanta la app compilada                   |
| `npm run lint`  | Corre ESLint sobre el codigo del frontend  |


## Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests de una clase especifica
pytest tests/clase_1/       # Solo Clase 1: Review Entity
pytest tests/clase_5/       # Solo Clase 5: SendReviewUseCase

# Ejecutar con cobertura
pytest --cov=src --cov-report=html

# Ejecutar tests verbose
pytest -v
```

## Ejemplo de Uso

```bash
# Ejecutar ejemplo basico (usa mocks, no requiere API keys)
python -m examples.basic_usage
```

```python
from src.application.use_cases.send_review import SendReviewUseCase
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository
from src.infrastructure.ai.mock_code_reviewer import MockCodeReviewer
from src.infrastructure.github.mock_github_adapter import MockGitHubAdapter

# Configurar adaptadores
repository = InMemoryReviewRepository()
code_reviewer = MockCodeReviewer(default_rating=85)
github_client = MockGitHubAdapter()

# Crear caso de uso
send_review = SendReviewUseCase(
    review_repository=repository,
    code_reviewer=code_reviewer,
    github_client=github_client,
)

# Enviar PR para revision
review = send_review.execute(pr_id="1")
print(f"Rating: {review.rating}")       # Rating(85)
print(f"Approved: {review.is_approved()}")  # True
```

## Las 8 Clases del Curso


| Clase | Componente                 | Capa            | Descripcion                           |
| ----- | -------------------------- | --------------- | ------------------------------------- |
| 1     | `Review`                   | Dominio         | Entidad principal: revision de codigo |
| 2     | `IReviewRepository`        | Puerto          | Interface para persistencia           |
| 3     | `ICodeReviewer`            | Puerto          | Interface para revisor IA             |
| 4     | `IGitHubClient`            | Puerto          | Interface para GitHub API             |
| 5     | `SendReviewUseCase`        | Aplicacion      | Enviar PR para revision               |
| 6     | `GetReviewResultUseCase`   | Aplicacion      | Obtener resultado de revision         |
| 7     | `ListReviewsUseCase`       | Aplicacion      | Listar todas las revisiones           |
| 8     | `InMemoryReviewRepository` | Infraestructura | Implementacion de persistencia        |


## Flujo de una Revision

1. **sendReview(pr_id)**: El usuario envia un PR para revision
2. El sistema obtiene el codigo del PR via **GitHub API** (puerto `IGitHubClient`)
3. El codigo se envia al **CodeReviewer** (puerto `ICodeReviewer`) que usa IA para evaluarlo
4. El agente IA califica el codigo (0-100) y genera recomendaciones
5. Si `rating > 70`: **Approved** con summary positivo
6. Si `rating <= 70`: **Rejected** con summary de mejoras necesarias
7. La revision se almacena via **Repository** (puerto `IReviewRepository`)
8. **getReviewResult(pr_id)**: Consulta el resultado almacenado
9. **listReviews()**: Lista el historial completo

## Stack Tecnologico

### Backend

| Tecnologia         | Uso                          |
| ------------------ | ---------------------------- |
| Python 3.11+       | Lenguaje principal           |
| FastAPI            | Framework HTTP para la API   |
| LangChain          | Framework para IA            |
| Claude (Anthropic) | Modelo de IA para revisiones |
| PyGithub           | Integracion con GitHub API   |
| Pydantic           | Validacion de datos          |
| pytest             | Testing                      |

### Frontend

| Tecnologia              | Uso                                       |
| ----------------------- | ----------------------------------------- |
| Next.js 16 (App Router) | Framework React con SSR / RSC             |
| React 19                | Libreria de UI                            |
| TypeScript 5            | Tipado estatico                           |
| Tailwind CSS v4         | Estilos utility-first                     |
| shadcn/ui + Radix UI    | Componentes accesibles                    |
| react-hook-form + zod   | Formularios y validacion                  |


## Progresion del Curso

El curso esta disenado para seguirse clase por clase:

- **Clase 1-2**: Fundamentos del dominio (entidades y puertos de persistencia)
- **Clase 3-4**: Puertos de integracion (IA y GitHub)
- **Clase 5-7**: Casos de uso (logica de aplicacion)
- **Clase 8**: Adaptadores de infraestructura (implementaciones concretas)

Cada clase tiene su propia carpeta de tests en `tests/clase_N/`, permitiendo validar el progreso de forma incremental.