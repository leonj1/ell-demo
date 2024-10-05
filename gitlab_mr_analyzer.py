import os
import re
import sys
import gitlab
from typing import List, Dict, Tuple
from urllib.parse import urlparse
import ell
from typing import List
from pydantic import BaseModel, Field

ell.init(verbose=False)

class CodeReview(BaseModel):
    code_review_score: int = Field(description="The code review score of the contents")
    make_it_succint: str = Field(description="If there are ways to make the code more concise. If there is no way to make it more concise, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_faster: str = Field(description="If there are ways to make the code faster. If there is no way to make it faster, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_secure: str = Field(description="If there are ways to make the code more secure. If there is no way to make it more secure, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_efficient: str = Field(description="If there are ways to make the code more efficient. If there is no way to make it more efficient, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_readable: str = Field(description="If there are ways to make the code more readable. If there is no way to make it more readable, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_testable: str = Field(description="If there are ways to make the code more testable. If there is no way to make it more testable, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")

class TestFileReview(BaseModel):
    is_test_file: bool = Field(description="Whether the file is a test file")
    review_score: int = Field(description="The test file review score of the contents")
    are_there_missing_test_scenarios: str = Field(description="List any missing test scenarios. If there are no missing test scenarios, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")

def parse_gitlab_mr_url(url: str) -> Tuple[str, int, int]:
    """
    Parse a GitLab merge request URL to extract the project path, project ID, and merge request IID.
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 5 or path_parts[-2] != 'merge_requests':
        raise ValueError("Invalid GitLab merge request URL")
    
    project_path = '/'.join(path_parts[:-3])
    mr_iid = int(path_parts[-1])
    
    return parsed_url.netloc, project_path, mr_iid

def checkout_merge_request(gl: gitlab.Gitlab, project_path: str, mr_iid: int) -> List[str]:
    """
    Checkout a merge request from GitLab and return a list of changed files.
    """
    project = gl.projects.get(project_path)
    mr = project.mergerequests.get(mr_iid)
    
    changes = mr.changes()['changes']
    return [change['new_path'] for change in changes]

def detect_programming_language(file_path: str) -> str:
    """
    Detect the programming language of a file based on its extension.
    """
    extension_to_language = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.cs': 'C#',
        '.rb': 'Ruby',
        '.go': 'Go',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.rs': 'Rust',
        '.scala': 'Scala',
        '.html': 'HTML',
        '.css': 'CSS',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.ps1': 'PowerShell',
        '.sql': 'SQL',
        '.tf': 'Terraform',
        '.tfvars': 'Terraform',
        '.tfstate': 'Terraform',
        '.tfstate.backup': 'Terraform',
        '.tfvars': 'Terraform',
        '.dockerfile': 'Docker',
        'Dockerfile': 'Docker',
    }
    
    _, ext = os.path.splitext(file_path)
    return extension_to_language.get(ext.lower(), 'Unknown')

def categorize_file(file_path: str) -> Tuple[str, str]:
    """
    Categorize a file as documentation, configuration, or code based on its extension and path.
    Also return the programming language for code files.
    """
    documentation_extensions = ['.md', '.txt', '.rst', '.adoc']
    configuration_extensions = ['.yml', '.yaml', '.json', '.ini', '.cfg', '.conf']
    
    _, ext = os.path.splitext(file_path)
    
    if ext in documentation_extensions or 'docs' in file_path.lower():
        return 'documentation', 'N/A'
    elif ext in configuration_extensions or 'config' in file_path.lower():
        return 'configuration', 'N/A'
    else:
        language = detect_programming_language(file_path)
        return 'code', language

def analyze_merge_request(gl: gitlab.Gitlab, project_path: str, mr_iid: int) -> Dict[str, List[Tuple[str, str]]]:
    """
    Analyze a merge request and categorize its files.
    """
    changed_files = checkout_merge_request(gl, project_path, mr_iid)
    
    categorized_files = {
        'documentation': [],
        'configuration': [],
        'code': []
    }
    
    for file_path in changed_files:
        category, language = categorize_file(file_path)
        categorized_files[category].append((file_path, language))
    
    return categorized_files

# create a function that will read the contents of standards/coding/*.txt where the input is the language and that will be the filename. The function should accept a cache of coding standards and first check to see if its already in the cache.
def read_coding_standards(language: str, cache: Dict[str, str]) -> str:
    """
    Read the contents of the coding standards file for a given programming language.
    """
    filename = f'standards/coding/{language.lower()}.txt'
    if filename not in cache:
        with open(filename, 'r') as file:
            cache[filename] = file.read()
    return cache[filename]

@ell.complex(model="gpt-4o-2024-08-06", response_format=CodeReview, temperature=0.1)
def code_reviewer(coding_standards: str, contents: str):
    return [
        ell.system(f"""
A good code reviewer plays a crucial role in maintaining code quality, 
sharing knowledge, and fostering a culture of continuous improvement 
within a development team:

# Technical Proficiency
Deep understanding of the programming language(s) being used
Familiarity with best practices and design patterns
Knowledge of the project's architecture and coding standards

# Attention to Detail
Ability to spot potential bugs, edge cases, and performance issues
Consistency in reviewing code thoroughly, not just skimming

# Constructive Communication
Provides clear, specific feedback
Explains the reasoning behind suggestions
Offers solutions or alternatives when pointing out issues

# Objectivity
Reviews code impartially, regardless of who wrote it
Focuses on the code, not the coder

# Mentorship Mindset
Uses code reviews as an opportunity to educate and share knowledge
Encourages good practices and helps team members grow

# Big Picture Awareness
Thinks about maintainability and scalability

# Security Consciousness
Identifies potential security vulnerabilities
Ensures that security best practices are followed

# Performance Consideration
Evaluates code for efficiency and potential performance impacts
Suggests optimizations where appropriate

# Positive Attitude
Acknowledges good work and clever solutions
Maintains a collaborative and supportive tone in comments

# Prioritization Skills
Distinguishes between critical issues and minor suggestions
Focuses on the most important aspects first

# Respect for Different Approaches
Recognizes that there can be multiple valid solutions to a problem
Open to discussion about different approaches.

{coding_standards}

Given the contents, you need to return a structured review.
    """
),
        ell.user(f"Analyze the following changes and provide feedback: {contents}.")
    ]

@ell.complex(model="gpt-4o-2024-08-06", response_format=TestFileReview)
def is_test_file(language:str, contents: str):
    """You are a movie review generator. Given the name of a movie, you need to return a structured review."""
    return [
        ell.system(f"""
You are a software developer. You are given the name of a programming language and 
the contents of a file. You need to determine if the file is a test file.
"""),
        ell.user(f"Analyze the following changes and provide feedback. Language: {language}, Contents: {contents}.")
    ]

# create a function that will accept a list of code review scores and return a single score
def calculate_final_score(scores: List[int]) -> int:
    """
    Calculate the final score based on the list of scores.
    """
    # if length of scores is 0, return 10
    if len(scores) == 0:
        return 10
    return sum(scores) / len(scores)

def print_review_details(file_path: str, language: str, review: CodeReview):
    """
    Print the details of a code review for a specific file.

    Args:
    file_path (str): The path of the file being reviewed.
    language (str): The programming language of the file.
    review (CodeReview): The CodeReview object containing the review details.
    """
    print(f"  - {file_path} (Language: {language})")
    print(f"    Code Review Score: {review.code_review_score}/10")
    
    if review.make_it_succint:
        print(f"    Make it more concise: {review.make_it_succint}")
    if review.make_it_faster:
        print(f"    Make it faster: {review.make_it_faster}")
    if review.make_it_more_secure:
        print(f"    Make it more secure: {review.make_it_more_secure}")
    if review.make_it_more_efficient:
        print(f"    Make it more efficient: {review.make_it_more_efficient}")
    if review.make_it_more_readable:
        print(f"    Make it more readable: {review.make_it_more_readable}")
    if review.make_it_more_testable:
        print(f"    Make it more testable: {review.make_it_more_testable}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python gitlab_mr_analyzer.py <GitLab_MR_URL>")
        sys.exit(1)

    mr_url = sys.argv[1]
    
    try:
        gitlab_domain, project_path, mr_iid = parse_gitlab_mr_url(mr_url)
        gitlab_url = f"https://{gitlab_domain}"
        
        # Initialize GitLab client
        gl = gitlab.Gitlab(gitlab_url, private_token=os.environ.get('GITLAB_TOKEN'))
        
        result = analyze_merge_request(gl, project_path, mr_iid)

        # read the contents of standards/coding/common.txt 
        with open('standards/coding/common.txt', 'r') as file:
            common_coding_standards = file.read()
            
        # create a variable that will be a cache of coding standards by programming language
        coding_standards_by_language = {}
        # create a list that will store the scores
        scores = []

        print(f"Merge Request Analysis for {mr_url}:")
        for category, files in result.items():
            print(f"\n{category.capitalize()}:")
            for file_path, language in files:
                if category == 'code':
                    # check to see if the coding standards file exists in standards/coding/
                    if not os.path.exists(f'standards/coding/{language.lower()}.txt'):
                        print(f"Warning: Coding standards file for {language} not found: {file_path}")
                        continue

                    # fetch the changes for file_path from the merge request in gitlab
                    mr = gl.projects.get(project_path).mergerequests.get(mr_iid)
                    changes = mr.changes()['changes']
                    for change in changes:
                        if change['new_path'] == file_path:
                            contents = change['diff']
                            break
                    else:
                        print(f"Error: File {file_path} not found in merge request changes.")
                        continue


                    review_message = is_test_file(language, contents)
                    review = review_message.parsed
                    if review.is_test_file:
                        if review.are_there_missing_test_scenarios:
                            print(f"  - {file_path} (Language: {language})")
                            print(f"    Code review score: {review.review_score}/10")
                            print(f"    Missing test scenarios: {review.are_there_missing_test_scenarios}")

                    coding_standards = common_coding_standards + read_coding_standards(language, coding_standards_by_language)
                    review_message = code_reviewer(coding_standards, contents)
                    review = review_message.parsed
                    scores.append(review.code_review_score)
                    print_review_details(file_path, language, review)
                else:
                    print(f"  - {file_path}")
        final_score = calculate_final_score(scores)
        print(f"Final Score: {final_score}/10")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except gitlab.exceptions.GitlabAuthenticationError:
        print("Error: GitLab authentication failed. Make sure GITLAB_TOKEN environment variable is set correctly.")
        sys.exit(1)
    except gitlab.exceptions.GitlabGetError:
        print("Error: Failed to retrieve merge request. Make sure the URL is correct and you have access to the project.")
        sys.exit(1)

if __name__ == "__main__":
    main()