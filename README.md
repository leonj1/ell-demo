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
    Make it more readable: Consider adding a comment or documentation to explain the purpose of the new 'buildContainerName' parameter in the 'waitForPodRunning' function for better understanding and maintainability. SHOULD
    Make it more testable: Ensure that the changes to the 'waitForPodRunning' function, with the addition of the 'buildContainerName' parameter, are covered by unit tests to verify its behavior in different scenarios. MUST
  - executors/kubernetes/kubernetes.go (Language: Go)
    Code Review Score: 8/10
    Make it more readable: Consider adding a comment explaining the purpose of the new parameter 'buildContainerName' in the 'waitForPodRunning' function call for better understanding of its role in the context. SHOULD
    Make it more testable: Ensure that the changes to the 'waitForPodRunning' function, particularly the addition of the 'buildContainerName' parameter, are covered by unit tests to verify that the function behaves correctly with this new input. MUST
  - executors/kubernetes/kubernetes_integration_test.go (Language: Go)
    Code Review Score: 8/10
    Make it more readable: Consider adding comments to explain the purpose of the new test function and its steps for better readability. SHOULD
    Make it more testable: Ensure that the new test function covers edge cases and potential failure scenarios to improve test coverage. SHOULD
  - executors/kubernetes/kubernetes_integration_test.go (Language: Go)
    Code Review Score: 8/10
    Make it more readable: Consider adding comments to the new test function to explain its purpose and the significance of the steps involved. SHOULD
    Make it more testable: Ensure that the new test function covers edge cases and potential failure scenarios. MAY
  - executors/kubernetes/util.go (Language: Go)
    Code Review Score: 8/10
    Make it more concise: The removal of the isPodReady function and its integration into isRunning is a good step towards conciseness. However, consider if the logic for checking container readiness can be further abstracted or simplified. MAY
    Make it more readable: The changes have improved readability by removing the isPodReady function and integrating its logic into isRunning. However, ensure that the use of variadic parameters (containers ...) is well-documented and understood by the team. MAY
    Make it more testable: The use of variadic parameters (containers ...) in functions like isRunning and getPodPhase can make testing more complex. Consider providing examples or test cases that cover different scenarios of container readiness. SHOULD
  - executors/kubernetes/util.go (Language: Go)
    Code Review Score: 8/10
    Make it more concise: The function isRunning could be simplified by using a map to track container readiness instead of nested loops, MAY.
    Make it faster: The use of nested loops in isRunning could be optimized by breaking early when all containers are found ready, SHOULD.
    Make it more efficient: Consider caching the pod status if it is fetched multiple times in a short period, MAY.
    Make it more readable: The code readability could be improved by adding comments explaining the logic in isRunning, MAY.
    Make it more testable: Ensure that the changes in isRunning and getPodPhase are covered by unit tests, especially with different combinations of container readiness, MUST.
  - executors/kubernetes/util_test.go (Language: Go)
    Code Review Score: 7/10
    Make it more concise: The removal of the TestIsPodReady function reduces redundancy, but ensure that its functionality is covered elsewhere. MAY
    Make it more readable: The changes improve readability by removing redundant code and simplifying test cases. The reduction of retries from 3 to 2 in TestWaitForPodRunning should be documented to explain the reasoning. SHOULD
    Make it more testable: Ensure that the removal of TestIsPodReady does not reduce test coverage. If necessary, integrate its logic into other tests. MUST
  - executors/kubernetes/util_test.go (Language: Go)
    Code Review Score: 7/10
    Make it more concise: The removal of the TestIsPodReady function reduces redundancy, but ensure that its functionality is covered elsewhere. SHOULD
    Make it more readable: The changes improve readability by removing redundant code and focusing on relevant test cases. The new TestIsRunning function is well-structured and clear. SHOULD
    Make it more testable: Ensure that the removal of TestIsPodReady does not reduce test coverage. The new TestIsRunning function adds valuable test cases. SHOULD
Warning: Coding standards file for Unknown not found: tests/dockerfiles/counter-service/Dockerfile
Final Score: 7.75/100
```
