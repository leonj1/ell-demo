from pydantic import BaseModel, Field
from models.comment import Comment

class TestFileReview(BaseModel):
    is_test_file: bool = Field(description="Whether the file is a test file")
    review_score: int = Field(description="The test file review score of the contents")
    are_there_missing_test_scenarios: Comment = Field(description="List any missing test scenarios. If there are no missing test scenarios, return an empty string. Do not state if the tests are good, only if there are areas of improvement.")
    