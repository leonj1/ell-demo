import os
import sys
import gitlab
import ell
from typing import List, Dict, Tuple
from typing import List
from llms import code_reviewer, is_test_file
from models.code_review import CodeReview
from models.summary import Summary
from vcs.gitlab import GitLab
from vcs.github import GitHub
from rich.table import Table
from rich.console import Console
from rich import box

ell.init(verbose=False)

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

# return a list of summaries
def print_review_details(file_path: str, language: str, review: CodeReview) -> List[Summary]:
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

    summaries: List[Summary] = []

    if review.make_it_succint:
        has_code_review = True
        my_table.add_row("Make it concise", review.make_it_succint.severity, review.make_it_succint.comment)
        if review.make_it_succint.severity == "MUST":
            summaries.append(Summary(category="Code Review", severity="MUST", recommendation=review.make_it_succint.comment, file_name=file_path))
    if review.make_it_faster:
        has_code_review = True
        my_table.add_row("Make it faster", review.make_it_faster.severity, review.make_it_faster.comment)
        if review.make_it_faster.severity == "MUST":
            summaries.append(Summary(category="Code Review", severity="MUST", recommendation=review.make_it_faster.comment, file_name=file_path))
    if review.make_it_more_secure:
        has_code_review = True
        my_table.add_row("Make it more secure", review.make_it_more_secure.severity, review.make_it_more_secure.comment)
        if review.make_it_more_secure.severity == "MUST":
            summaries.append(Summary(category="Code Review", severity="MUST", recommendation=review.make_it_more_secure.comment, file_name=file_path))
    if review.make_it_more_efficient:
        has_code_review = True
        my_table.add_row("Make it more efficient", review.make_it_more_efficient.severity, review.make_it_more_efficient.comment)
        if review.make_it_more_efficient.severity == "MUST":
            summaries.append(Summary(category="Code Review", severity="MUST", recommendation=review.make_it_more_efficient.comment, file_name=file_path))
    if review.make_it_more_readable:
        has_code_review = True
        my_table.add_row("Make it more readable", review.make_it_more_readable.severity, review.make_it_more_readable.comment)
        if review.make_it_more_readable.severity == "MUST":
            summaries.append(Summary(category="Code Review", severity="MUST", recommendation=review.make_it_more_readable.comment, file_name=file_path))
    if review.make_it_more_testable:
        has_code_review = True
        my_table.add_row("Make it more testable", review.make_it_more_testable.severity, review.make_it_more_testable.comment)
        if review.make_it_more_testable.severity == "MUST":
            summaries.append(Summary(category="Code Review", severity="MUST", recommendation=review.make_it_more_testable.comment, file_name=file_path))

    if has_code_review:
        console.print(my_table)

    return summaries

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
    
    # a collection of summaries of type Summary     
    summaries: List[Summary] = []

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
                        if review.are_there_missing_test_scenarios.comment != "":
                            table_header = f"Test File Review for {file_path} (Language: {language})"
                            console = Console()
                            my_table = Table(title=table_header)
                            my_table.add_column("Category", justify="left", style="red", no_wrap=True)
                            my_table.add_column("Severity", justify="center", style="red", no_wrap=True)
                            my_table.add_column("Recommendation", style="green", no_wrap=False)
                            my_table.add_row("Review of Test", review.are_there_missing_test_scenarios.severity, review.are_there_missing_test_scenarios.comment)
                            console.print(my_table)
                            if review.are_there_missing_test_scenarios.severity == "MUST":
                                summaries.append(Summary(category="Test", severity="MUST", recommendation=review.are_there_missing_test_scenarios.comment, file_name=file_path))

                    coding_standards = common_coding_standards + read_coding_standards(language, coding_standards_by_language)
                    review_message = code_reviewer(coding_standards, contents)
                    review = review_message.parsed
                    scores.append(review.code_review_score)
                    summaries.extend(print_review_details(file_path, language, review))
                else:
                    print(f"  - {file_path}")

        if has_code_changes and not has_tests:
            print("CRITICAL: No test files detected.")

        final_score = calculate_final_score(scores)
        print(f"Final Score: {final_score}/10")
        if len(summaries) > 0:
            console = Console()
            my_table = Table(title="Summary of MUST Findings", show_lines=True, box=box.MINIMAL_DOUBLE_HEAD)
            my_table.add_column("Category", justify="left", style="red", no_wrap=True)
            my_table.add_column("Severity", justify="center", style="red", no_wrap=True)
            my_table.add_column("File", style="white", no_wrap=False)
            my_table.add_column("Recommendation", style="green", no_wrap=False)
            for summary in summaries:
                my_table.add_row(summary.category, summary.severity, summary.file_name, summary.recommendation)
            console.print(my_table)

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