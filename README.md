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

## Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests de una clase especifica
pytest tests/clase_1/       # Solo Clase 1: Review Entity

# Ejecutar langraph
langgraph dev