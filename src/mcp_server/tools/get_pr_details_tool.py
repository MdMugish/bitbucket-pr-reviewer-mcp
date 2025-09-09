from typing import Dict, Any
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService


def register_get_pr_details_tool(mcp: FastMCP, bitbucket_service: BitbucketService):
    @mcp.tool()
    async def get_pr_details(pr_id: str, repository: str) -> Dict[str, Any]:
        try:
            pr = await bitbucket_service.get_pr_details(pr_id, repository)
            return {
                "id": pr.id,
                "title": pr.title,
                "description": pr.description,
                "author": pr.author,
                "status": pr.status,
                "repository": pr.repository,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "source_branch": pr.source_branch,
                "destination_branch": pr.destination_branch
            }
        except Exception as e:
            return {"error": f"Failed to get PR details: {str(e)}"}
