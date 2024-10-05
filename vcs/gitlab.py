import gitlab
from urllib.parse import urlparse
from typing import List
from vcs.version_control import VersionControl

class GitLab(VersionControl):
    def __init__(self, mr_url: str):
        self.mr_url = mr_url
        self.parsed_url = ""
        self.path_parts = "" 
        self.project_url_path = ""
        self.request_id = ""

    def domain(self) -> str:
        """
        Parse a GitLab merge request URL to extract the project path, project ID, and merge request IID.
        """
        if self.parsed_url != "":
            return self.parsed_url.netloc

        self.parsed_url = urlparse(self.mr_url)
        self.path_parts = self.parsed_url.path.strip('/').split('/')

        if len(self.path_parts) < 5 or self.path_parts[-2] != 'merge_requests':
            raise ValueError("Invalid GitLab merge request URL")
        
        # project_path = '/'.join(path_parts[:-3])
        # mr_iid = int(path_parts[-1])
        
        return self.parsed_url.netloc

    def project_path(self) -> str:
        if self.project_url_path != "":
            return self.project_url_path

        self.domain
        
        self.project_url_path = '/'.join(self.path_parts[:-3])
        return self.project_url_path

    def change_id(self) -> str:
        if self.request_id != "":
            return self.request_id

        self.domain
        
        self.request_id = self.path_parts[-1]
        return self.request_id

    def client(self, url: str, token: str):
        return gitlab.Gitlab(url, private_token=token)
    
    def checkout_changes(self, vcs_client: gitlab.Gitlab, project_path: str, mr_iid: int) -> List[str]:
        project = vcs_client.projects.get(project_path)
        mr = project.mergerequests.get(mr_iid)
        
        changes = mr.changes()['changes']
        return [change['new_path'] for change in changes]