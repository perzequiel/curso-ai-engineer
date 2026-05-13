"""Value Object: Rating - Calificacion de una revision de codigo."""

APPROVAL_THRESHOLD = 70


class Rating:
    """Representa la calificacion numerica de una revision (0-100)."""

    def __init__(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError(f"Rating must be between 0 and 100, got {value}")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def is_passing(self) -> bool:
        """Determina si la calificacion supera el umbral de aprobacion (70)."""
        return self._value > APPROVAL_THRESHOLD

    def __repr__(self) -> str:
        return f"Rating({self._value})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Rating):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)
