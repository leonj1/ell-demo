from pydantic import BaseModel, Field

class Comment(BaseModel):
    comment: str = Field(description="The comment to be added to the code review. If there is no comment, return an empty string.")
    severity: str = Field(description="The severity of the comment. Must be one of MUST, SHOULD, or MAY.")
