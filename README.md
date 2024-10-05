# GitLab MR Analyzer

This project analyzes GitLab Merge Requests using AI to provide code reviews and suggestions.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A GitLab account with access to the repository you want to analyze
- A GitLab Personal Access Token with API access

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gitlab-mr-analyzer.git
   cd gitlab-mr-analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add your GitLab Personal Access Token:
   ```
   GITLAB_TOKEN=your_personal_access_token_here
   ```

## Usage

Run the script with the following command:
```
python gitlab_mr_analyzer.py https://gitlab.com/gitlab-org/gitlab-runner/-/merge_requests/5039
```

Output will be:
```
Merge Request Analysis for https://gitlab.com/gitlab-org/gitlab-runner/-/merge_requests/5039:

Documentation:
  - tests/dockerfiles/README.md

Configuration:

Code:
  - executors/kubernetes/kubernetes.go (Language: Go)
    Code Review Score: 8/10
    Make it more readable: Consider adding a comment explaining the purpose of the new 'buildContainerName' parameter in the 'waitForPodRunning' function for better clarity and maintainability. SHOULD
    Make it more testable: Ensure that the changes to the 'waitForPodRunning' function, including the new 'buildContainerName' parameter, are covered by unit tests to verify correct behavior. MUST
  - executors/kubernetes/kubernetes_integration_test.go (Language: Go)
    Code Review Score: 8/10
    Make it more readable: Consider adding comments to the new test function to explain its purpose and the significance of the steps being performed. SHOULD
    Make it more testable: Ensure that the new test function covers all possible edge cases and scenarios related to the service stopping. MAY
  - executors/kubernetes/util.go (Language: Go)
    Code Review Score: 8/10
    Make it more concise: The function isRunning can be made more succinct by using a map to track container readiness instead of nested loops. SHOULD
    Make it faster: The nested loops in isRunning could be optimized by breaking early when a container is found ready. MAY
    Make it more efficient: The isRunning function could use a map for container statuses to reduce the time complexity from O(n*m) to O(n+m). SHOULD
    Make it more readable: The removal of isPodReady and the addition of container-specific readiness checks improves readability by making the code more explicit about what it checks. However, consider adding comments to explain the logic in isRunning. SHOULD
    Make it more testable: The changes make the code more testable by allowing specific containers to be checked for readiness, which can be tested individually. No further changes needed. SHOULD
  - executors/kubernetes/util_test.go (Language: Go)
    Code Review Score: 7/10
    Make it more concise: The removal of the TestIsPodReady function reduces redundancy and simplifies the codebase, which is a positive change. However, ensure that the functionality covered by TestIsPodReady is adequately tested elsewhere. SHOULD
    Make it more readable: The changes made improve readability by removing redundant code and focusing on relevant test cases. The new TestIsRunning function is well-structured and easy to follow. SHOULD
    Make it more testable: Ensure that the removal of TestIsPodReady does not lead to a gap in test coverage. Consider adding similar test cases to other relevant test functions if necessary. SHOULD
Warning: Coding standards file for Unknown not found: tests/dockerfiles/counter-service/Dockerfile
Final Score: 7.75/10
```
