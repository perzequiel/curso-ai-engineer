"""Ejemplo basico de uso del sistema de Code Review.

Demuestra el flujo completo usando adaptadores mock:
1. Enviar un PR para revision
2. Obtener el resultado
3. Listar todas las revisiones
"""

from src.application.use_cases.send_review import SendReviewUseCase
from src.application.use_cases.get_review_result import GetReviewResultUseCase
from src.application.use_cases.list_reviews import ListReviewsUseCase
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository
from src.infrastructure.ai.mock_code_reviewer import MockCodeReviewer
from src.infrastructure.github.mock_github_adapter import MockGitHubAdapter


def main():
    # 1. Configurar adaptadores (inyeccion de dependencias)
    repository = InMemoryReviewRepository()
    code_reviewer = MockCodeReviewer(default_rating=85)
    github_client = MockGitHubAdapter()

    # 2. Crear casos de uso
    send_review = SendReviewUseCase(
        review_repository=repository,
        code_reviewer=code_reviewer,
        github_client=github_client,
    )
    get_result = GetReviewResultUseCase(review_repository=repository)
    list_reviews = ListReviewsUseCase(review_repository=repository)

    # 3. Enviar PR #1 para revision
    print("=" * 60)
    print("Enviando PR #1 para revision...")
    review1 = send_review.execute(pr_id="1")
    print(f"  Review ID: {review1.id}")
    print(f"  Status: {review1.status.value}")
    print(f"  Rating: {review1.rating}")
    print(f"  Approved: {review1.is_approved()}")
    print(f"  Summary: {review1.summary}")
    print(f"  Recommendations: {review1.recommendations}")

    # 4. Enviar PR #2 para revision
    print("\n" + "=" * 60)
    print("Enviando PR #2 para revision...")
    review2 = send_review.execute(pr_id="2")
    print(f"  Review ID: {review2.id}")
    print(f"  Status: {review2.status.value}")
    print(f"  Rating: {review2.rating}")
    print(f"  Approved: {review2.is_approved()}")

    # 5. Obtener resultado de PR #1
    print("\n" + "=" * 60)
    print("Obteniendo resultado de PR #1...")
    result = get_result.execute(pr_id="1")
    print(f"  PR ID: {result.pr_id}")
    print(f"  Rating: {result.rating}")

    # 6. Listar todas las revisiones
    print("\n" + "=" * 60)
    print("Listando todas las revisiones:")
    all_reviews = list_reviews.execute()
    for r in all_reviews:
        status = "APPROVED" if r.is_approved() else "REJECTED"
        print(f"  - PR #{r.pr_id}: {r.rating} ({status})")

    print("\n" + "=" * 60)
    print("Ejemplo completado exitosamente!")


if __name__ == "__main__":
    main()
