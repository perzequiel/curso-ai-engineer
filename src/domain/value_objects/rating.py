APPROVAL_THRESHOLD = 70


class Rating:
    def __init__(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError(f"Rating must be between 0 - 100 , got {value}")

        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def is_passing(self) -> bool:
        return self._value >= APPROVAL_THRESHOLD
