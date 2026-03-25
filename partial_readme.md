# Curso AI Engineer - Code Review System

## Overview

Sistema de revision de codigo automatizado con IA usando arquitectura **Ports & Adapters** (Hexagonal Architecture). Separa la logica de negocio de la infraestructura mediante puertos (interfaces) y adaptadores (implementaciones).

El sistema recibe Pull Requests, los analiza con un agente de IA, y genera una calificacion con recomendaciones. Si el rating es mayor a 70, el PR es aprobado; caso contrario, es rechazado.

## Estructura de Carpetas

```
curso-ai-engineer/
│
├── curso_AI.md                              # Especificacion del curso
├── partial_readme.md                        # Este archivo
├── README.md                                # Documentacion completa
├── pyproject.toml                           # Configuracion y dependencias
├── .env.example                             # Variables de entorno
├── .gitignore
│
├── src/
│   │
│   ├── domain/                              # Nucleo de negocio
│   │   ├── entities/
│   │   │   └── review.py                    # Clase 1: Review
│   │   ├── value_objects/
│   │   │   ├── review_status.py             # ReviewStatus enum
│   │   │   └── rating.py                    # Rating (0-100)
│   │   └── ports/
│   │       ├── review_repository.py         # Clase 2: IReviewRepository
│   │       ├── code_reviewer.py             # Clase 3: ICodeReviewer
│   │       └── github_client.py             # Clase 4: IGitHubClient
│   │
│   ├── application/
│   │   └── use_cases/
│   │       ├── send_review.py               # Clase 5: SendReviewUseCase
│   │       ├── get_review_result.py         # Clase 6: GetReviewResultUseCase
│   │       └── list_reviews.py              # Clase 7: ListReviewsUseCase
│   │
│   └── infrastructure/
│       ├── persistence/
│       │   └── in_memory_repository.py      # Clase 8: InMemoryReviewRepository
│       ├── github/
│       │   └── github_adapter.py            # GitHubAdapter + Mock
│       ├── ai/
│       │   └── ai_code_reviewer.py          # AICodeReviewer + Mock
│       └── processors/
│           └── parallel_processor.py        # Analisis estatico con astroid
│
├── tests/
│   ├── conftest.py                          # Fixtures compartidas
│   ├── clase_1/test_review.py
│   ├── clase_2/test_review_repository.py
│   ├── clase_3/test_code_reviewer.py
│   ├── clase_4/test_github_client.py
│   ├── clase_5/test_send_review.py
│   ├── clase_6/test_get_review_result.py
│   ├── clase_7/test_list_reviews.py
│   └── clase_8/test_in_memory_repository.py
│
└── examples/
    └── basic_usage.py                       # Ejemplo de uso con mocks
```
