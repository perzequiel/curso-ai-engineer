from abc import ABC, abstractmethod

class ICodeReviewer(ABC):
  @abstractmethod
  def review_code(self):
    None

  @abstractmethod
  def get_review_rules(self):
    None

class CodeContent(ABC):
  def __init__(self, files: dict[str,str], folder_structure:list[str], pr_title: str, pr_description: str):
    self.files = files
    self.folder_structure = folder_structure
    self.pr_title = pr_title
    self.pr_description = pr_description

class ReviewResult():
  def __init__(self, rating: int, summary: str, recommendations: list[str]):
    self.rating = rating
    self.summary = summary
    self.recommendations = recommendations