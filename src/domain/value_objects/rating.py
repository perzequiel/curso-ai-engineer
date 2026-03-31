class Rating:
    _THRESHOLD = 70
    def __init__(self, value):
        self.value = value

    def is_passing(self) -> bool:
        return self.value > self._THRESHOLD