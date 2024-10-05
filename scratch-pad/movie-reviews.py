import ell
from pydantic import BaseModel, Field

class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie")
    rating: int = Field(description="The rating of the movie out of 10")
    summary: str = Field(description="A brief summary of the movie")

@ell.complex(model="gpt-4o-2024-08-06", response_format=MovieReview)
def generate_movie_review(movie: str):
    """You are a movie review generator. Given the name of a movie, you need to return a structured review."""
    return f"Generate a review for the movie {movie}"

review_message = generate_movie_review("The Prestige")
review = review_message.parsed
print(f"Movie: {review.title}, Rating: {review.rating}/10")
print(f"Summary: {review.summary}")

