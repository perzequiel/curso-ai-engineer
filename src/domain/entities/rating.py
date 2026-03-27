from enum import Enum

class RatingThreshold(Enum):
    MINIMUM_APPROVED = 71

class Rating:
    """Clase que encapsula la lógica de evaluación de ratings."""
    
    def __init__(self, value: int):
        if value < 0 or value > 100:
            raise ValueError("Rating must be between 0 and 100")
        self.value = value
    
    def is_approved(self) -> bool:
        """Determina si el rating es suficiente para aprobar."""
        return self.value >= RatingThreshold.MINIMUM_APPROVED.value
    
    def __repr__(self) -> str:
        return f"Rating(value={self.value})"
