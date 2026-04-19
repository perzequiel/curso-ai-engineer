from abc import ABC, abstractmethod

class ICodeReviewer(ABC):
  @abstractmethod
  def review_code(self):
    None

  @abstractmethod
  def get_review_rules(self):
    None

class CodeContent(ABC):
  None

class ReviewResult():
  def __init__(self, rating: int, summary: str, recommendations: list[str]):
    self.rating = rating
    self.summary = summary
    self.recommendations = recommendations