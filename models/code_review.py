from pydantic import BaseModel, Field
from models.comment import Comment

class CodeReview(BaseModel):
    code_review_score: int = Field(description="The code review score of the contents. Must be between 0 and 10.")
    make_it_succint: Comment = Field(description="If there are ways to make the code more concise. If there is no way to make it more concise, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_faster: Comment = Field(description="If there are ways to make the code faster. If there is no way to make it faster, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_secure: Comment = Field(description="If there are ways to make the code more secure. If there is no way to make it more secure, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_efficient: Comment = Field(description="If there are ways to make the code more efficient. If there is no way to make it more efficient, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_readable: Comment = Field(description="If there are ways to make the code more readable. If there is no way to make it more readable, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_testable: Comment = Field(description="If there are ways to make the code more testable. If there is no way to make it more testable, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
