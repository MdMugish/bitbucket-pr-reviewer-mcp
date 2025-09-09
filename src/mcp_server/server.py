from fastmcp import FastMCP
from config.settings import Settings
from services.bitbucket_service import BitbucketService
from services.matching_service import MatchingService
from services.sanitization_service import SanitizationService
from mcp_server.tools.list_prs_tool import register_list_prs_tool
from mcp_server.tools.review_pr_tool import register_review_pr_tool
from mcp_server.tools.post_comments_tool import register_post_comments_tool
from mcp_server.tools.get_pr_details_tool import register_get_pr_details_tool
from mcp_server.tools.auto_post_comments_tool import register_auto_post_comments_tool
from mcp_server.tools.integrated_review_tool import register_integrated_review_tool
from mcp_server.tools.enhanced_review_tool import register_enhanced_review_tool
from mcp_server.tools.enhanced_auto_review_tool import register_enhanced_auto_review_tool


def create_server(settings: Settings) -> FastMCP:
    mcp = FastMCP("Bitbucket PR Reviewer")
    
    bitbucket_service = BitbucketService(settings)
    matching_service = MatchingService()
    sanitization_service = SanitizationService(settings)
    
    register_list_prs_tool(mcp, bitbucket_service)
    register_review_pr_tool(mcp, bitbucket_service, matching_service, sanitization_service)
    register_post_comments_tool(mcp, bitbucket_service)
    register_get_pr_details_tool(mcp, bitbucket_service)
    register_auto_post_comments_tool(mcp, bitbucket_service)
    register_integrated_review_tool(mcp, bitbucket_service, sanitization_service)
    register_enhanced_review_tool(mcp, bitbucket_service, sanitization_service)
    register_enhanced_auto_review_tool(mcp, bitbucket_service, matching_service, sanitization_service)
    
    return mcp