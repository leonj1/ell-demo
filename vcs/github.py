from urllib.parse import urlparse
from vcs.version_control import VersionControl
from github import Github
from typing import List, Dict


class GitHub(VersionControl):
    def __init__(self, mr_url: str):
        self.mr_url = mr_url

    def domain(self) -> str:
        """
        Parse a GitHub pull request URL to extract the domain.
        """
        parsed_url = urlparse(self.mr_url)
        return parsed_url.netloc

    def project_path(self) -> str:
        """
        Extract the project path from the GitHub pull request URL.
        """
        parsed_url = urlparse(self.mr_url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) < 4 or path_parts[-2] != 'pull':
            raise ValueError("Invalid GitHub pull request URL")
        
        return '/'.join(path_parts[:2])

    def change_id(self) -> str:
        """
        Extract the pull request number from the GitHub pull request URL.
        """
        parsed_url = urlparse(self.mr_url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) < 4 or path_parts[-2] != 'pull':
            raise ValueError("Invalid GitHub pull request URL")
        
        return path_parts[-1]

    def client(self, url: str, token: str):
        """
        Create and return a GitHub client instance.
        """
        return Github(token)

    def checkout_changes(self, vcs_client: Github, project_path: str, pr_number: str) -> List[Dict]:
        """
        Fetch the changes for a given pull request.
        """
        repo = vcs_client.get_repo(project_path)
        pull_request = repo.get_pull(int(pr_number))
        
        changes = []
        for file in pull_request.get_files():
            changes.append({
                'new_path': file.filename,
                'diff': file.patch
            })
        
        return changes
