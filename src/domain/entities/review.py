class Review:
    def __init__(self, pr_id: str):
        self.pr_id = pr_id
        self.status = "pending"
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.id = not None
