# Dominio - Code Review System

Representacion visual del dominio de la aplicacion usando diagramas Mermaid.

## Diagrama de Clases

```mermaid
classDiagram
    direction TB

    %% ──────────────────────────────────────
    %% VALUE OBJECTS
    %% ──────────────────────────────────────

    class ReviewStatus {
        <<enumeration>>
        PENDING
        IN_PROGRESS
        COMPLETED
        FAILED
    }

    class Rating {
        <<value object>>
        -int _value
        +int value
        +is_passing() bool
        +__eq__(other) bool
        +__hash__() int
    }

    %% ──────────────────────────────────────
    %% ENTIDAD PRINCIPAL
    %% ──────────────────────────────────────

    class Review {
        <<entity>>
        +str id
        +str pr_id
        +ReviewStatus status
        +Rating rating
        +str summary
        +list~str~ recommendations
        +datetime created_at
        +datetime completed_at
        +is_approved() bool
        +complete(rating, summary, recommendations) void
        +fail(reason) void
        +start_processing() void
    }

    %% ──────────────────────────────────────
    %% DATA TRANSFER OBJECTS
    %% ──────────────────────────────────────

    class CodeContent {
        <<dataclass>>
        +dict~str, str~ files
        +list~str~ folder_structure
        +str pr_title
        +str pr_description
    }

    class ReviewResult {
        <<dataclass>>
        +int rating
        +str summary
        +list~str~ recommendations
    }

    class PRFile {
        <<dataclass>>
        +str filename
        +str content
        +str status
        +str patch
    }

    class PRInfo {
        <<dataclass>>
        +str pr_id
        +str title
        +str description
        +str author
        +list~PRFile~ files
        +list~str~ folder_structure
    }

    %% ──────────────────────────────────────
    %% PUERTOS (INTERFACES)
    %% ──────────────────────────────────────

    class IReviewRepository {
        <<interface>>
        +save(review: Review) Review
        +find_by_pr_id(pr_id: str) Review | None
        +find_by_id(review_id: str) Review | None
        +find_all() list~Review~
        +delete(review_id: str) bool
    }

    class ICodeReviewer {
        <<interface>>
        +review_code(code: CodeContent) ReviewResult
        +get_review_rules() list~str~
    }

    class IGitHubClient {
        <<interface>>
        +get_pr_code(pr_id: str) PRInfo
        +get_pr_files(pr_id: str) list~PRFile~
        +post_review_comment(pr_id: str, comment: str) bool
    }

    %% ──────────────────────────────────────
    %% CASOS DE USO
    %% ──────────────────────────────────────

    class SendReviewUseCase {
        <<use case>>
        -IReviewRepository _review_repository
        -ICodeReviewer _code_reviewer
        -IGitHubClient _github_client
        +execute(pr_id: str) Review
    }

    class GetReviewResultUseCase {
        <<use case>>
        -IReviewRepository _review_repository
        +execute(pr_id: str) Review
    }

    class ListReviewsUseCase {
        <<use case>>
        -IReviewRepository _review_repository
        +execute() list~Review~
    }

    class ReviewNotFoundError {
        <<exception>>
    }

    %% ──────────────────────────────────────
    %% ADAPTADORES (INFRAESTRUCTURA)
    %% ──────────────────────────────────────

    class InMemoryReviewRepository {
        <<adapter>>
        -dict~str, Review~ _reviews
        +save(review: Review) Review
        +find_by_pr_id(pr_id: str) Review | None
        +find_by_id(review_id: str) Review | None
        +find_all() list~Review~
        +delete(review_id: str) bool
        +clear() void
    }

    class GitHubAdapter {
        <<adapter>>
        -str _token
        -str _repo_name
        +get_pr_code(pr_id: str) PRInfo
        +get_pr_files(pr_id: str) list~PRFile~
        +post_review_comment(pr_id: str, comment: str) bool
    }

    class MockGitHubAdapter {
        <<adapter mock>>
        -dict~str, PRInfo~ _mock_prs
        +get_pr_code(pr_id: str) PRInfo
        +get_pr_files(pr_id: str) list~PRFile~
        +post_review_comment(pr_id: str, comment: str) bool
    }

    class AICodeReviewer {
        <<adapter>>
        -str _api_key
        -str _model
        -list~str~ _rules
        +review_code(code: CodeContent) ReviewResult
        +get_review_rules() list~str~
    }

    class MockCodeReviewer {
        <<adapter mock>>
        -int _default_rating
        -list~str~ _rules
        +review_code(code: CodeContent) ReviewResult
        +get_review_rules() list~str~
    }

    %% ──────────────────────────────────────
    %% RELACIONES - Dominio
    %% ──────────────────────────────────────

    Review *-- ReviewStatus : status
    Review *-- Rating : rating
    IReviewRepository ..> Review : gestiona
    ICodeReviewer ..> CodeContent : recibe
    ICodeReviewer ..> ReviewResult : retorna
    IGitHubClient ..> PRInfo : retorna
    IGitHubClient ..> PRFile : retorna
    PRInfo o-- PRFile : contiene

    %% ──────────────────────────────────────
    %% RELACIONES - Casos de Uso -> Puertos
    %% ──────────────────────────────────────

    SendReviewUseCase --> IReviewRepository : usa
    SendReviewUseCase --> ICodeReviewer : usa
    SendReviewUseCase --> IGitHubClient : usa
    GetReviewResultUseCase --> IReviewRepository : usa
    GetReviewResultUseCase ..> ReviewNotFoundError : lanza
    ListReviewsUseCase --> IReviewRepository : usa

    %% ──────────────────────────────────────
    %% RELACIONES - Adaptadores implementan Puertos
    %% ──────────────────────────────────────

    InMemoryReviewRepository ..|> IReviewRepository : implementa
    GitHubAdapter ..|> IGitHubClient : implementa
    MockGitHubAdapter ..|> IGitHubClient : implementa
    AICodeReviewer ..|> ICodeReviewer : implementa
    MockCodeReviewer ..|> ICodeReviewer : implementa
```

## Diagrama de Arquitectura Hexagonal

```mermaid
graph TB
    subgraph EXTERNAL["Mundo Exterior"]
        USER["Usuario"]
        GITHUB_API["GitHub API"]
        CLAUDE_API["Claude API<br/>(Anthropic)"]
        DB["Base de Datos"]
    end

    subgraph ADAPTERS_IN["Adaptadores de Entrada"]
        API["API / CLI"]
    end

    subgraph APPLICATION["Capa de Aplicacion"]
        UC1["SendReviewUseCase"]
        UC2["GetReviewResultUseCase"]
        UC3["ListReviewsUseCase"]
    end

    subgraph DOMAIN["Dominio"]
        REVIEW["Review"]
        RATING["Rating"]
        STATUS["ReviewStatus"]
        REVIEW --- RATING
        REVIEW --- STATUS
    end

    subgraph PORTS["Puertos"]
        P1["IReviewRepository"]
        P2["ICodeReviewer"]
        P3["IGitHubClient"]
    end

    subgraph ADAPTERS_OUT["Adaptadores de Salida"]
        A1["InMemoryReviewRepository"]
        A2["AICodeReviewer<br/>(LangChain + Claude)"]
        A3["GitHubAdapter<br/>(PyGithub)"]
    end

    USER --> API
    API --> UC1
    API --> UC2
    API --> UC3

    UC1 --> P1
    UC1 --> P2
    UC1 --> P3
    UC2 --> P1
    UC3 --> P1

    UC1 -.-> REVIEW
    UC2 -.-> REVIEW
    UC3 -.-> REVIEW

    P1 --> A1
    P2 --> A2
    P3 --> A3

    A1 --> DB
    A2 --> CLAUDE_API
    A3 --> GITHUB_API

    style DOMAIN fill:#2d5016,stroke:#4a8c1c,color:#fff
    style PORTS fill:#1a3a5c,stroke:#2980b9,color:#fff
    style APPLICATION fill:#5b2c6f,stroke:#8e44ad,color:#fff
    style ADAPTERS_OUT fill:#7d3c00,stroke:#e67e22,color:#fff
    style ADAPTERS_IN fill:#7d3c00,stroke:#e67e22,color:#fff
    style EXTERNAL fill:#4a4a4a,stroke:#888,color:#fff
```

## Diagrama de Flujo - sendReview(pr_id)

```mermaid
flowchart TD
    START([Usuario envia PR]) --> CREATE[Crear Review<br/>status: PENDING]
    CREATE --> PROCESS[start_processing<br/>status: IN_PROGRESS]
    PROCESS --> SAVE1[("Guardar en Repository")]
    SAVE1 --> FETCH["Obtener codigo del PR<br/>via IGitHubClient"]

    FETCH --> BUILD["Construir CodeContent<br/>(files, folder_structure, title, description)"]
    BUILD --> REVIEW["Enviar a ICodeReviewer<br/>review_code(code)"]

    REVIEW --> RESULT["Recibir ReviewResult<br/>(rating, summary, recommendations)"]
    RESULT --> DECISION{rating > 70?}

    DECISION -->|SI| APPROVED["complete()<br/>status: COMPLETED<br/>Approved Summary"]
    DECISION -->|NO| REJECTED["complete()<br/>status: COMPLETED<br/>Rejected Summary"]

    APPROVED --> SAVE2[("Guardar en Repository")]
    REJECTED --> SAVE2

    FETCH -->|Error| FAIL["fail(reason)<br/>status: FAILED"]
    REVIEW -->|Error| FAIL
    FAIL --> SAVE3[("Guardar en Repository")]

    SAVE2 --> END([Retornar Review])
    SAVE3 --> END

    style APPROVED fill:#1a5c1a,stroke:#2ecc71,color:#fff
    style REJECTED fill:#7d1a1a,stroke:#e74c3c,color:#fff
    style FAIL fill:#7d1a1a,stroke:#e74c3c,color:#fff
    style DECISION fill:#7d6b00,stroke:#f1c40f,color:#fff
```

## Diagrama de Estados - Review

```mermaid
stateDiagram-v2
    [*] --> PENDING : Review creada

    PENDING --> IN_PROGRESS : start_processing()

    IN_PROGRESS --> COMPLETED : complete(rating, summary, recommendations)
    IN_PROGRESS --> FAILED : fail(reason)

    COMPLETED --> [*]
    FAILED --> [*]

    state COMPLETED {
        [*] --> CheckRating
        CheckRating --> Approved : rating > 70
        CheckRating --> Rejected : rating <= 70
    }
```

## Mapa de Dependencias por Capa

```mermaid
graph LR
    subgraph Domain["Dominio (sin dependencias externas)"]
        E["Review<br/>Rating<br/>ReviewStatus"]
        P["IReviewRepository<br/>ICodeReviewer<br/>IGitHubClient"]
        DTO["CodeContent<br/>ReviewResult<br/>PRFile / PRInfo"]
    end

    subgraph Application["Aplicacion (depende solo del Dominio)"]
        UC["SendReviewUseCase<br/>GetReviewResultUseCase<br/>ListReviewsUseCase"]
    end

    subgraph Infrastructure["Infraestructura (depende del Dominio)"]
        AD["InMemoryReviewRepository<br/>GitHubAdapter<br/>AICodeReviewer<br/>MockGitHubAdapter<br/>MockCodeReviewer"]
    end

    UC --> E
    UC --> P
    UC --> DTO
    AD --> P
    AD --> E

    Infrastructure -.->|nunca| Application

    style Domain fill:#2d5016,stroke:#4a8c1c,color:#fff
    style Application fill:#5b2c6f,stroke:#8e44ad,color:#fff
    style Infrastructure fill:#7d3c00,stroke:#e67e22,color:#fff
```
