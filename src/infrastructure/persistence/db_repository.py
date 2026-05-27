"""Adaptador de persistencia Postgres (pgvector) para IReviewRepository.

Implementacion intercambiable con InMemoryReviewRepository: cumple el mismo
puerto, asi que los casos de uso y la API no cambian al hacer el switch.

Cada operacion abre una sesion corta (unit of work) y la cierra. Esto evita
acoplar el ciclo de vida de la sesion al request de FastAPI y mantiene el
adaptador autocontenido.
"""

from __future__ import annotations

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, select

from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository
from src.infrastructure.persistence.models import ReviewModel


class DBReviewRepository(IReviewRepository):
    """Repositorio de revisiones respaldado por Postgres + pgvector."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, review: Review) -> Review:
        """Inserta o actualiza una revision (upsert por id)."""
        with self._session_factory() as session:
            model = session.get(ReviewModel, review.id)
            if model is None:
                model = ReviewModel.from_domain(review)
                session.add(model)
            else:
                model.apply_domain(review)
            session.commit()
            session.refresh(model)
            return model.to_domain()

    def find_by_pr_id(self, pr_id: str) -> Review | None:
        """Busca la revision mas reciente de un Pull Request."""
        with self._session_factory() as session:
            stmt = (
                select(ReviewModel)
                .where(ReviewModel.pr_id == pr_id)
                .order_by(ReviewModel.created_at.desc())
            )
            model = session.exec(stmt).first()
            return model.to_domain() if model else None

    def find_by_id(self, review_id: str) -> Review | None:
        """Busca una revision por su id unico."""
        with self._session_factory() as session:
            model = session.get(ReviewModel, review_id)
            return model.to_domain() if model else None

    def find_all(self) -> list[Review]:
        """Retorna todas las revisiones ordenadas por fecha de creacion."""
        with self._session_factory() as session:
            stmt = select(ReviewModel).order_by(ReviewModel.created_at)
            return [m.to_domain() for m in session.exec(stmt).all()]

    def delete(self, review_id: str) -> bool:
        """Elimina una revision. Retorna True si existia."""
        with self._session_factory() as session:
            model = session.get(ReviewModel, review_id)
            if model is None:
                return False
            session.delete(model)
            session.commit()
            return True

    def clear(self) -> None:
        """Borra todas las revisiones. Util para testing."""
        with self._session_factory() as session:
            for model in session.exec(select(ReviewModel)).all():
                session.delete(model)
            session.commit()

    # -- Extra (fuera del puerto): busqueda semantica con pgvector ---------

    def find_similar(
        self, embedding: list[float], top_k: int = 5
    ) -> list[Review]:
        """Busqueda por similitud coseno sobre el embedding del summary.

        Usa el operador `<=>` de pgvector via `cosine_distance`. Solo devuelve
        filas que tengan embedding. No forma parte de IReviewRepository: es una
        capacidad adicional que aprovecha la columna pgvector.
        """
        with self._session_factory() as session:
            stmt = (
                select(ReviewModel)
                .where(ReviewModel.embedding.is_not(None))
                .order_by(ReviewModel.embedding.cosine_distance(embedding))
                .limit(top_k)
            )
            return [m.to_domain() for m in session.exec(stmt).all()]
