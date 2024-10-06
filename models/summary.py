from pydantic import BaseModel, Field

class Summary(BaseModel):
    category: str = Field(description="The category of the summary.")
    severity: str = Field(description="The severity of the comment. Must be one of MUST, SHOULD, or MAY.")
    recommendation: str = Field(description="The recommendation of the comment. If there is no recommendation, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    file_name: str = Field(description="The file name of the review.")
