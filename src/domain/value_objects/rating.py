APPROVAL_THRESHOLD = 70

class Rating:
  def __init__(self, value: int):
    if value < 0 or value > 100:
      raise ValueError(f"Wrong value rating: {value} - It must be between 0 and 100")
    self._value = value

  @property
  def value(self) -> int:
      return self._value

  def is_approved(self) -> bool:
    return self._value >= APPROVAL_THRESHOLD