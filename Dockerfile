# syntax=docker/dockerfile:1.6

# ---------- Builder: instala dependencias con uv en un venv reutilizable ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# `uv sync` ignora VIRTUAL_ENV por defecto y crea/usa `.venv/` en el cwd.
# `--active` le indica que use el venv apuntado por VIRTUAL_ENV (/opt/venv),
# de lo contrario los paquetes se instalan en /app/.venv y el stage runtime
# termina copiando un venv vacio (sin fastapi-cli, uvicorn, etc.).
RUN uv venv /opt/venv \
    && VIRTUAL_ENV=/opt/venv uv sync --frozen --no-install-project --no-dev --active

# ---------- Runtime: imagen final sin toolchain de build ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV=/opt/venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app \
    && useradd --system --gid app --home /app app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY --chown=app:app main.py ./
COPY --chown=app:app src ./src

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/docs >/dev/null || exit 1

CMD ["fastapi", "run", "src/infrastructure/api/http_api.py", "--host", "0.0.0.0", "--port", "8000"]
