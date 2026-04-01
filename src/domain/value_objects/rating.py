class Rating:

    THRESHOLD = 70

    def __init__(self, value: int):
        self.value = value

    def in_range(self):
        return self.value > self.THRESHOLD

