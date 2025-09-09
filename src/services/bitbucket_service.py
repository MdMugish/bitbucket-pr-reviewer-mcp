import asyncio
from typing import List, Optional
from atlassian import Bitbucket
from models.pull_request import PullRequest
from config.settings import Settings


class BitbucketService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.bitbucket = Bitbucket(
            url="https://api.bitbucket.org/",
            username=settings.bitbucket.username,
            password=settings.bitbucket.app_password
        )

    async def get_all_pull_requests(self) -> List[PullRequest]:
        try:
            all_prs = []
            for repository in self.settings.bitbucket.repositories:
                # Convert generator to list
                prs_data = list(self.bitbucket.get_pull_requests(
                    project_key=self.settings.bitbucket.workspace,
                    repository_slug=repository,
                    state="OPEN"
                ))
                
                for pr_data in prs_data:
                    pr = PullRequest(
                        id=str(pr_data["id"]),
                        title=pr_data["title"],
                        description=pr_data.get("description", ""),
                        author=pr_data["author"]["display_name"],
                        status=pr_data["state"],
                        repository=repository,
                        created_at=pr_data["created_on"],
                        updated_at=pr_data["updated_on"],
                        source_branch=pr_data.get("source", {}).get("branch", {}).get("name"),
                        destination_branch=pr_data.get("destination", {}).get("branch", {}).get("name")
                    )
                    all_prs.append(pr)
            
            return all_prs
        except Exception as e:
            raise Exception(f"Failed to fetch pull requests: {str(e)}")

    async def get_pr_details(self, pr_id: str, repository: str) -> PullRequest:
        try:
            pr_data = self.bitbucket.get_pull_request(
                project_key=self.settings.bitbucket.workspace,
                repository_slug=repository,
                pull_request_id=pr_id
            )
            
            return PullRequest(
                id=str(pr_data["id"]),
                title=pr_data["title"],
                description=pr_data.get("description", ""),
                author=pr_data["author"]["display_name"],
                status=pr_data["state"],
                repository=repository,
                created_at=pr_data["created_on"],
                updated_at=pr_data["updated_on"],
                source_branch=pr_data.get("source", {}).get("branch", {}).get("name"),
                destination_branch=pr_data.get("destination", {}).get("branch", {}).get("name")
            )
        except Exception as e:
            raise Exception(f"Failed to fetch PR details: {str(e)}")

    async def get_pr_diff(self, pr_id: str, repository: str) -> str:
        try:
            # Get the pull request first to get the diff URL
            pr_data = self.bitbucket.get_pull_request(
                project_key=self.settings.bitbucket.workspace,
                repository_slug=repository,
                pull_request_id=pr_id
            )
            
            # Extract diff URL from the PR links
            diff_url = pr_data['links']['diff']['href']
            
            # Fetch the diff using requests
            import requests
            response = requests.get(
                diff_url, 
                auth=(self.settings.bitbucket.username, self.settings.bitbucket.app_password)
            )
            
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"Failed to fetch diff: HTTP {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Failed to fetch PR diff: {str(e)}")

    async def post_comment(self, pr_id: str, repository: str, comment: str, line_number: Optional[int] = None, file_path: Optional[str] = None) -> bool:
        try:
            # Use direct API call to avoid atlassian-python-api parameter issues
            import requests
            url = f"https://api.bitbucket.org/2.0/repositories/{self.settings.bitbucket.workspace}/{repository}/pullrequests/{pr_id}/comments"
            
            payload = {
                "content": {
                    "raw": comment
                }
            }
            
            # Add inline comment if line number and file path are provided
            if line_number and file_path:
                payload["inline"] = {
                    "path": file_path,
                    "from": line_number
                }
            
            response = requests.post(
                url,
                json=payload,
                auth=(self.settings.bitbucket.username, self.settings.bitbucket.app_password),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                return True
            else:
                raise Exception(f"API call failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"Failed to post comment: {str(e)}")

    async def get_pr_comments(self, pr_id: str, repository: str) -> List[dict]:
        """
        Get all comments for a PR to check if it's already reviewed by AI.
        """
        try:
            import requests
            url = f"https://api.bitbucket.org/2.0/repositories/{self.settings.bitbucket.workspace}/{repository}/pullrequests/{pr_id}/comments"
            
            response = requests.get(
                url,
                auth=(self.settings.bitbucket.username, self.settings.bitbucket.app_password),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("values", [])
            else:
                raise Exception(f"Failed to fetch comments: HTTP {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Failed to fetch PR comments: {str(e)}")

    async def get_all_prs(self) -> List[PullRequest]:
        """
        Alias for get_all_pull_requests for consistency.
        """
        return await self.get_all_pull_requests()
