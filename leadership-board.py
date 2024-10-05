import ell
from typing import List

ell.init(verbose=True)

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def onboarding_specialist(goal : str):
    """
You are a Senior Technical Onboarding Specialist
Persona: Sarah, 35, with 10 years of software development experience across various roles and technologies.
Skillset:

Extensive knowledge of software development lifecycles
Strong communication and teaching skills
Familiarity with multiple programming languages and frameworks
Experience in creating technical documentation and training materials
Expected Outcome: Streamlined onboarding process, reducing time-to-productivity for new hires by 30%.
Only respond in 1 paragraph.
"""
    return f"Write a proposal on how would you accomplish {goal}"

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def developer_experience_engineer(goal : str):
    """
Developer Experience (DX) Engineer
Persona: Alex, 28, a former full-stack developer with a passion for optimizing developer workflows.
Skillset:
Proficiency in CI/CD pipelines and DevOps practices
Experience with various developer tools and environments
Strong problem-solving skills
Knowledge of performance optimization techniques
Expected Outcome: 20% increase in developer productivity through optimized workflows and tools.
Only respond in 1 paragraph.
"""
    return f"Write a proposal on how would you accomplish {goal}"

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def knowledge_management_specialist(goal : str):
    """
Knowledge Management Specialist
Persona: Priya, 32, with a background in technical writing and information architecture.
Skillset:

Excellent writing and editing skills
Experience with knowledge base systems and documentation tools
Understanding of information architecture and user experience
Familiarity with software development concepts
Expected Outcome: Comprehensive, easily accessible knowledge base, reducing time spent searching for information by 25%.
Only respond in 1 paragraph.
"""
    return f"Write a proposal on how would you accomplish {goal}"
 
@ell.simple(model="gpt-4o-mini", temperature=1.0)
def technical_mentor_coordinator(goal : str):
    """
Technical Mentor Coordinator
Persona: Michael, 40, a seasoned developer with strong interpersonal skills and a knack for nurturing talent.
Skillset:

Extensive software development experience
Strong leadership and mentoring abilities
Good understanding of career development in tech
Experience in conflict resolution and team dynamics
Expected Outcome: Improved knowledge sharing and 15% increase in employee satisfaction and retention rates.
Only respond in 1 paragraph.
"""
    return f"Write a proposal on how would you accomplish {goal}"


@ell.simple(model="gpt-4o", temperature=0.1)
def choose_the_best_draft(drafts : List[str]):
    """You are an expert fiction editor."""
    return f"Choose the best draft from the following list: {'\n'.join(drafts)}."

@ell.simple(model="gpt-4-turbo", temperature=0.2)
def business_strategy_plan(about : str):
    """
    You are an experience Chief Technology Officer.
    You are a strategic thinker and planner. With Ability to envision long term goals and create an actionable plan to achieve them.
    You have experience in guiding teams and influencing C-suite executives.
    You have excellent written and verbal skills, adept at presenting complex ideas clearly.
    Financial acumen: Strong understanding of budgeting, forecasting, and ROI analysis.
    You write with an active voice.
    """
    # Note: You can pass in api_params to control the language model call
    # in the case n = 4 tells OpenAI to generate a batch of 4 outputs.
    onboarding_ideas = onboarding_specialist(about, api_params=(dict(n=4)))
    developer_experience_engineer_ideas = developer_experience_engineer(about, api_params=(dict(n=4)))
    knowledge_management_specialist_ideas = knowledge_management_specialist(about, api_params=(dict(n=4)))
    technical_mentor_coordinator_ideas = technical_mentor_coordinator(about, api_params=(dict(n=4)))

    best_onboarding_draft = choose_the_best_draft(onboarding_ideas)
    best_developer_experience_engineer_draft = choose_the_best_draft(developer_experience_engineer_ideas)
    best_knowledge_management_specialist_draft = choose_the_best_draft(knowledge_management_specialist_ideas)
    best_technical_mentor_coordinator_draft = choose_the_best_draft(technical_mentor_coordinator_ideas)

    return f"Create a strategy proposal to other leaders that will include the problem statement, value proposition, execution plan, and contingency plan in your voice: {[
        best_onboarding_draft,
        best_developer_experience_engineer_draft,
        best_knowledge_management_specialist_draft,
        best_technical_mentor_coordinator_draft]}."

story = business_strategy_plan("""
Become the single place where developers go for training and design assistance in 2 years. 
Create a seamless and supportive entry path for new hires that accelerates their time to productivity and job satisfaction.
Have standards that increase the quality of developer and engineer output.
""")

print(story)