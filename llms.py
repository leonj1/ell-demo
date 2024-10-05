import ell
from models.code_review import CodeReview
from models.test_file_review import TestFileReview

ell.init(verbose=False)

@ell.complex(model="gpt-4o-2024-08-06", response_format=CodeReview, temperature=0.1)
def code_reviewer(coding_standards: str, contents: str):
    """
    Perform a code review based on the given coding standards and file contents.
    """
    prompt = f"""
    You are an expert code reviewer. Please review the following code based on the provided coding standards.
    
    Coding Standards:
    {coding_standards}
    
    Code to review:
    {contents}
    
    Provide a detailed code review addressing the following aspects:
    1. Overall code quality (score out of 10)
    2. Suggestions to make the code more concise
    3. Suggestions to make the code faster
    4. Suggestions to make the code more secure
    5. Suggestions to make the code more efficient
    6. Suggestions to make the code more readable
    7. Suggestions to make the code more testable
    
    Format your response as a CodeReview object.
    """
    
    return prompt

@ell.complex(model="gpt-4o-2024-08-06", response_format=TestFileReview)
def is_test_file(language:str, contents: str):
    """Determine if a file is a test file based on its contents and language."""
    return [
        ell.system(f"""
You are a software developer. You are given the name of a programming language and 
the contents of a file. You need to determine if the file is a test file.
"""),
        ell.user(f"Analyze the following changes and provide feedback. Language: {language}, Contents: {contents}.")
    ]

__all__ = ['code_reviewer', 'is_test_file']
