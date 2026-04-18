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
  None