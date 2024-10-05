import os
import sys
import gitlab
from typing import List, Dict, Tuple
import ell
from typing import List
from pydantic import BaseModel, Field
from llms import code_reviewer, is_test_file
from vcs.gitlab import GitLab
from vcs.github import GitHub
from rich.table import Table
from rich.console import Console

ell.init(verbose=False)

class Comment(BaseModel):
    comment: str = Field(description="The comment to be added to the code review. If there is no comment, return an empty string.")
    severity: str = Field(description="The severity of the comment. Must be one of MUST, SHOULD, or MAY.")

class CodeReview(BaseModel):
    code_review_score: int = Field(description="The code review score of the contents. Must be between 0 and 10.")
    make_it_succint: Comment = Field(description="If there are ways to make the code more concise. If there is no way to make it more concise, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_faster: Comment = Field(description="If there are ways to make the code faster. If there is no way to make it faster, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_secure: Comment = Field(description="If there are ways to make the code more secure. If there is no way to make it more secure, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_efficient: Comment = Field(description="If there are ways to make the code more efficient. If there is no way to make it more efficient, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_readable: Comment = Field(description="If there are ways to make the code more readable. If there is no way to make it more readable, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")
    make_it_more_testable: Comment = Field(description="If there are ways to make the code more testable. If there is no way to make it more testable, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")

class TestFileReview(BaseModel):
    is_test_file: bool = Field(description="Whether the file is a test file")
    review_score: int = Field(description="The test file review score of the contents")
    are_there_missing_test_scenarios: str = Field(description="List any missing test scenarios. If there are no missing test scenarios, return an empty string. If there is a recommendation end with either MUST, SHOULD, or MAY.")

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

def analyze_merge_request(changed_files: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    """
    Analyze a merge request and categorize its files.
    """
    
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
    table_header = f"Score: {review.code_review_score}/10: {file_path}"

    has_code_review = False
    console = Console()
    my_table = Table(title=table_header)
    my_table.add_column("Category", justify="left", style="cyan", no_wrap=True)
    my_table.add_column("Severity", justify="left", style="red", no_wrap=True)
    my_table.add_column("Recommendation", style="green", no_wrap=False)
    
    if review.make_it_succint:
        has_code_review = True
        my_table.add_row("Make it concise", review.make_it_succint.severity, review.make_it_succint.comment)
    if review.make_it_faster:
        has_code_review = True
        my_table.add_row("Make it faster", review.make_it_faster.severity, review.make_it_faster.comment)
    if review.make_it_more_secure:
        has_code_review = True
        my_table.add_row("Make it more secure", review.make_it_more_secure.severity, review.make_it_more_secure.comment)
    if review.make_it_more_efficient:
        has_code_review = True
        my_table.add_row("Make it more efficient", review.make_it_more_efficient.severity, review.make_it_more_efficient.comment)
    if review.make_it_more_readable:
        has_code_review = True
        my_table.add_row("Make it more readable", review.make_it_more_readable.severity, review.make_it_more_readable.comment)
    if review.make_it_more_testable:
        has_code_review = True
        my_table.add_row("Make it more testable", review.make_it_more_testable.severity, review.make_it_more_testable.comment)
        
    if has_code_review:
        console.print(my_table)

def main():
    if len(sys.argv) != 2:
        print("Usage: python gitlab_mr_analyzer.py <GitLab_MR_URL>")
        sys.exit(1)

    mr_url = sys.argv[1]
    
    # if mr_url is a github url, then use the GitHub class
    if 'github.com' in mr_url:
        vcs = GitHub(mr_url)
        token = os.environ.get('GITHUB_TOKEN')
    else:
        vcs = GitLab(mr_url)
        token = os.environ.get('GITLAB_TOKEN')
    
    try:
        domain = vcs.domain()
        project_path = vcs.project_path()
        mr_iid = vcs.change_id()
        
        vcs_client = vcs.client(domain, token)

        changed_files_resp = vcs.checkout_changes(vcs_client, project_path, mr_iid)
        changed_files = [change['new_path'] for change in changed_files_resp]
        result = analyze_merge_request(changed_files)

        # read the contents of standards/coding/common.txt 
        with open('standards/coding/common.txt', 'r') as file:
            common_coding_standards = file.read()
            
        coding_standards_by_language = {}
        scores = []
        has_code_changes = False
        has_tests = False

        print(f"Merge Request Analysis for {mr_url}:")
        for category, files in result.items():
            print(f"\n{category.capitalize()}:")
            for file_path, language in files:
                if category == 'code':
                    has_code_changes = True
                    # check to see if the coding standards file exists in standards/coding/
                    if not os.path.exists(f'standards/coding/{language.lower()}.txt'):
                        print(f"Warning: Coding standards file for {language} not found: {file_path}")
                        continue

                    changes = vcs.checkout_changes(vcs_client, project_path, mr_iid)
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
                        has_tests = True
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

        if has_code_changes and not has_tests:
            print("CRITICAL: No test files detected.")

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