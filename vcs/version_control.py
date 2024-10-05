from abc import ABC, abstractmethod
import gitlab
from typing import List

class VersionControl(ABC):
    @abstractmethod
    def domain(self) -> float:
        """Return the domain for the version control system."""
        pass

    @abstractmethod
    def project_path(self) -> float:
        """Return the project path for the version control system."""
        pass

    @abstractmethod
    def change_id(self) -> str:
        """Return the merge request or pull request id for the version control system."""
        pass
    
    @abstractmethod
    def client(self, url: str, token: str):
        """Return the client for the version control system."""
        pass
    
    @abstractmethod
    def checkout_changes(self, vcs_client: gitlab.Gitlab, project_path: str, mr_iid: int) -> List[str]:
        """Return the changes for the merge request or pull request."""
        pass