import ell
from typing import List

ell.init(verbose=True)

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def generate_topic_ideas(about : str):
    """You are graduate level professor of psychology. Only answer in a single sentence."""
    return f"Generate a topic idea for a research paper about {about}."

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def write_a_draft_of_a_presentation(idea : str):
    """You are an adept story writer. The story should only be 500 words."""
    return f"Write a resarch paper about {idea}."

@ell.simple(model="gpt-4o", temperature=0.1)
def choose_the_best_presentation(drafts : List[str]):
    """You are an expert non-fiction editor."""
    return f"Choose the best draft from the following list: {'\n'.join(drafts)}."

@ell.simple(model="gpt-4-turbo", temperature=0.2)
def write_a_really_good_presentation(about : str):
    """You are a professional psychiastrist that writes in the style of Dr. Phillip Stall, MD."""
    ideas = generate_topic_ideas(about, api_params=(dict(n=4)))
    drafts = [write_a_draft_of_a_presentation(idea) for idea in ideas]
    best_draft = choose_the_best_presentation(drafts)
    return f"Make a final revision that covers 1000 word research paper in your voice: {best_draft}."

presentation = write_a_really_good_presentation("Anxiety and Co-occurring Disorders. what are the anxiety disorders? What is anxiety and its related disorders? What are the treatments? How do disorders related to substance use?")

print(presentation)
