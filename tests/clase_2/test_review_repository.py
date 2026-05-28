"""Clase 2: Tests para el puerto IReviewRepository.

Verifica que la interface abstracta define correctamente
el contrato que deben cumplir los repositorios.
"""

from abc import ABC

import pytest

from src.domain.ports.review_repository import IReviewRepository

class TestIReviewRepositoryInterface:
    """Tests para verificar la interface del repositorio."""

    def test_is_abstract_class(self):
        assert issubclass(IReviewRepository, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            IReviewRepository()

    def test_defines_save_method(self):
        assert hasattr(IReviewRepository, "save")

    def test_defines_find_by_pr_id_method(self):
        assert hasattr(IReviewRepository, "find_by_pr_id")

    def test_defines_find_by_id_method(self):
        assert hasattr(IReviewRepository, "find_by_id")

    def test_defines_find_all_method(self):
        assert hasattr(IReviewRepository, "find_all")

    def test_defines_delete_method(self):
        assert hasattr(IReviewRepository, "delete")

    def test_incomplete_implementation_raises_error(self):
        """Una implementacion incompleta no puede instanciarse."""

        class IncompleteRepo(IReviewRepository):
            def save(self, review):
                pass

        with pytest.raises(TypeError):
            IncompleteRepo()

    def test_complete_implementation_can_instantiate(self):
        """Una implementacion completa puede instanciarse."""

        class CompleteRepo(IReviewRepository):
            def save(self, review):
                return review

            def find_by_pr_id(self, pr_id):
                return None

            def find_by_id(self, review_id):
                return None

            def find_all(self):
                return []

            def delete(self, review_id):
                return False

        repo = CompleteRepo()
        assert isinstance(repo, IReviewRepository)
