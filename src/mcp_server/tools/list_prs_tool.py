from typing import List, Dict, Any
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService


def register_list_prs_tool(mcp: FastMCP, bitbucket_service: BitbucketService):
    @mcp.tool()
    async def list_pull_requests() -> Dict[str, Any]:
        try:
            prs = await bitbucket_service.get_all_pull_requests()
            
            # Group PRs by repository
            grouped_prs = {}
            for pr in prs:
                if pr.repository not in grouped_prs:
                    grouped_prs[pr.repository] = []
                grouped_prs[pr.repository].append({
                    "id": pr.id,
                    "title": pr.title,
                    "author": pr.author,
                    "status": pr.status,
                    "repository": pr.repository,
                    "created_at": pr.created_at.isoformat(),
                    "description": pr.description[:100] + "..." if len(pr.description) > 100 else pr.description
                })
            
            return {
                "total_repositories": len(grouped_prs),
                "total_prs": len(prs),
                "repositories": grouped_prs
            }
        except Exception as e:
            return {"error": f"Failed to fetch pull requests: {str(e)}"}
