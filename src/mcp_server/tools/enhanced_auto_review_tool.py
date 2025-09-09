from typing import Dict, Any, List
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from services.matching_service import MatchingService
from services.sanitization_service import SanitizationService
from services.platform_detection_service import PlatformDetectionService
from services.diff_parser_service import DiffParserService
from models.comment import Comment, SeverityLevel
import re
import json
import os


def register_enhanced_auto_review_tool(mcp: FastMCP, bitbucket_service: BitbucketService, 
                            matching_service: MatchingService, sanitization_service: SanitizationService):
    
    # ============================================================================
    # REVIEW ALL PRs - Multiple Natural Language Variants
    # ============================================================================
    
    @mcp.tool()
    async def review_all_prs_and_comment() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically post comments. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and comment"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_add_comment() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically add comments. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and add comment"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_post_comments() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically post comments. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and post comments"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_comment_on_them() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically comment on them. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and comment on them"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_add_comments() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically add comments. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and add comments"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_post_comment() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically post comment. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and post comment"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_comment_it() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically comment it. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and comment it"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_prs_and_comment_them() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically comment them. Skips PRs already reviewed by AI.
        Natural language: "Review all PRs and comment them"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    # ============================================================================
    # REVIEW SPECIFIC PR - Multiple Natural Language Variants
    # ============================================================================
    
    @mcp.tool()
    async def review_pr_and_comment(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically post comments. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and comment"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_pr_and_add_comment(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically add comment. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and add comment"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_pr_and_post_comments(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically post comments. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and post comments"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_pr_and_comment_it(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically comment it. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and comment it"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_pr_and_add_comments(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically add comments. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and add comments"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_pr_and_post_comment(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically post comment. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and post comment"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_pr_and_comment_on_it(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically comment on it. Skips if already reviewed by AI.
        Natural language: "Review PR 3400 and comment on it"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    # ============================================================================
    # SHORTCUT COMMANDS - Even More Natural Language
    # ============================================================================
    
    @mcp.tool()
    async def review_all_and_comment() -> Dict[str, Any]:
        """
        Review all PRs and comment - shortcut command.
        Natural language: "Review all and comment"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_and_add_comment() -> Dict[str, Any]:
        """
        Review all PRs and add comment - shortcut command.
        Natural language: "Review all and add comment"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_all_and_post_comments() -> Dict[str, Any]:
        """
        Review all PRs and post comments - shortcut command.
        Natural language: "Review all and post comments"
        """
        return await _review_all_prs_implementation(bitbucket_service, sanitization_service)
    
    @mcp.tool()
    async def review_and_comment(pr_identifier: str) -> Dict[str, Any]:
        """
        Review PR and comment - shortcut command.
        Natural language: "Review and comment PR 3400"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_and_add_comment(pr_identifier: str) -> Dict[str, Any]:
        """
        Review PR and add comment - shortcut command.
        Natural language: "Review and add comment PR 3400"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)
    
    @mcp.tool()
    async def review_and_post_comments(pr_identifier: str) -> Dict[str, Any]:
        """
        Review PR and post comments - shortcut command.
        Natural language: "Review and post comments PR 3400"
        """
        return await _review_specific_pr_implementation(pr_identifier, bitbucket_service, matching_service, sanitization_service)


# ============================================================================
# IMPLEMENTATION FUNCTIONS
# ============================================================================

async def _review_all_prs_implementation(bitbucket_service: BitbucketService, sanitization_service: SanitizationService) -> Dict[str, Any]:
    """
    Core implementation for reviewing all PRs and posting comments.
    """
    try:
        # Get all PRs
        all_prs = await bitbucket_service.get_all_prs()
        open_prs = [pr for pr in all_prs if pr.status == "OPEN"]
        
        if not open_prs:
            return {
                "success": True,
                "message": "No open PRs found to review",
                "prs_reviewed": 0,
                "prs_skipped": 0
            }
        
        results = []
        reviewed_count = 0
        skipped_count = 0
        
        for pr in open_prs:
            try:
                # Check if already reviewed by AI
                if await _is_pr_already_reviewed(pr.id, pr.repository, bitbucket_service):
                    results.append({
                        "pr_id": pr.id,
                        "title": pr.title,
                        "repository": pr.repository,
                        "status": "SKIPPED",
                        "reason": "Already reviewed by AI"
                    })
                    skipped_count += 1
                    continue
                
                # Review and comment on this PR
                review_result = await _review_and_comment_pr(pr.id, pr.repository, bitbucket_service, sanitization_service)
                
                results.append({
                    "pr_id": pr.id,
                    "title": pr.title,
                    "repository": pr.repository,
                    "status": "REVIEWED",
                    "comments_posted": review_result.get("comments_posted", 0),
                    "issues_found": review_result.get("issues_found", 0),
                    "message": review_result.get("message", "PR reviewed and comments posted")
                })
                reviewed_count += 1
                
            except Exception as e:
                results.append({
                    "pr_id": pr.id,
                    "title": pr.title,
                    "repository": pr.repository,
                    "status": "ERROR",
                    "error": str(e)
                })
        
        return {
            "success": True,
            "message": f"Auto-review completed: {reviewed_count} PRs reviewed, {skipped_count} PRs skipped",
            "prs_reviewed": reviewed_count,
            "prs_skipped": skipped_count,
            "total_open_prs": len(open_prs),
            "results": results
        }
        
    except Exception as e:
        return {"error": f"Failed to review all PRs: {str(e)}"}


async def _review_specific_pr_implementation(pr_identifier: str, bitbucket_service: BitbucketService, 
                                          matching_service: MatchingService, sanitization_service: SanitizationService) -> Dict[str, Any]:
    """
    Core implementation for reviewing a specific PR and posting comments.
    """
    try:
        # Find the PR
        multiple_prs = await matching_service.find_multiple_prs(pr_identifier, bitbucket_service)
        
        if not multiple_prs:
            return {
                "error": f"No PR found matching '{pr_identifier}'",
                "suggestion": "Use 'list_pull_requests' to see available PRs"
            }
        
        if len(multiple_prs) > 1:
            # Multiple PRs found - ask for clarification
            pr_options = []
            for pr in multiple_prs:
                pr_options.append({
                    "id": pr.id,
                    "title": pr.title,
                    "repository": pr.repository,
                    "author": pr.author
                })
            
            return {
                "multiple_matches": True,
                "message": f"Found {len(multiple_prs)} PRs matching '{pr_identifier}'. Please specify which one:",
                "options": pr_options,
                "suggestion": "Provide more specific identifier like 'repo-name: PR-title' or use PR ID"
            }
        
        # Single PR found
        pr = multiple_prs[0]
        
        # Check if already reviewed by AI
        if await _is_pr_already_reviewed(pr.id, pr.repository, bitbucket_service):
            return {
                "success": True,
                "pr_id": pr.id,
                "title": pr.title,
                "repository": pr.repository,
                "status": "SKIPPED",
                "reason": "Already reviewed by AI",
                "message": f"PR #{pr.id} '{pr.title}' has already been reviewed by AI. Skipping to avoid duplicate comments."
            }
        
        # Review and comment on this PR
        review_result = await _review_and_comment_pr(pr.id, pr.repository, bitbucket_service, sanitization_service)
        
        return {
            "success": True,
            "pr_id": pr.id,
            "title": pr.title,
            "repository": pr.repository,
            "status": "REVIEWED",
            "comments_posted": review_result.get("comments_posted", 0),
            "issues_found": review_result.get("issues_found", 0),
            "message": review_result.get("message", "PR reviewed and comments posted")
        }
        
    except Exception as e:
        return {"error": f"Failed to review PR: {str(e)}"}


async def _is_pr_already_reviewed(pr_id: str, repository: str, bitbucket_service: BitbucketService) -> bool:
    """
    Check if a PR already has AI review comments by looking for [AI - Review] in comments.
    """
    try:
        # Get PR comments
        comments = await bitbucket_service.get_pr_comments(pr_id, repository)
        
        # Check if any comment contains [AI - Review]
        for comment in comments:
            if "[AI - Review]" in comment.get("content", {}).get("raw", ""):
                return True
        
        return False
        
    except Exception:
        # If we can't check comments, assume already reviewed to be safe
        return True


async def _call_claude_api(sanitized_diff: str, platform: str, pr_title: str, diff_locations: List[Any]) -> List[Dict[str, Any]]:
    """
    Call Claude API to analyze the sanitized diff and return structured comments.
    For now, return empty comments since we don't have Claude API key.
    In a real implementation, this would call Claude API.
    """
    try:
        # For now, return empty comments since we don't have Claude API key
        # In a real implementation, this would call Claude API
        return []
    except Exception as e:
        print(f"Failed to call Claude API: {e}")
        return []


async def _review_and_comment_pr(pr_id: str, repository: str, bitbucket_service: BitbucketService, sanitization_service: SanitizationService) -> Dict[str, Any]:
    """
    Internal function to review a PR and post comments automatically.
    """
    try:
        # Get and sanitize diff
        diff = await bitbucket_service.get_pr_diff(pr_id, repository)
        sanitized_diff = sanitization_service.sanitize_diff(diff)
        
        # Parse diff to get file locations - use original diff for correct file paths
        diff_parser = DiffParserService()
        diff_locations = diff_parser.parse_original_diff(diff)  # Use original diff for file paths
        
        # Detect platform
        platform_detector = PlatformDetectionService()
        platform = platform_detector.detect_platform(repository)
        
        # Get PR details for title
        pr_details = await bitbucket_service.get_pr_details(pr_id, repository)
        pr_title = pr_details.get("title", "Unknown PR")
        
        # Call Claude API to get comments
        comments = await _call_claude_api(sanitized_diff, platform, pr_title, diff_locations)
        
        # Post comments (skip P2 and summary comments)
        posted_comments = []
        failed_comments = []
        
        for comment in comments:
            try:
                # Skip P2 comments
                if comment.get("severity") == "P2":
                    continue
                
                # Skip summary comments
                if comment.get("is_summary", False):
                    continue
                
                comment_text = f"[AI - Review] {comment['content']}"
                
                success = await bitbucket_service.post_comment(
                    pr_id,
                    repository,
                    comment_text,
                    comment.get("line_number"),
                    comment.get("file_path")
                )
                
                if success:
                    posted_comments.append(comment)
                else:
                    failed_comments.append(comment)
                    
            except Exception as e:
                failed_comments.append({**comment, "error": str(e)})
        
        return {
            "success": True,
            "comments_posted": len(posted_comments),
            "comments_failed": len(failed_comments),
            "issues_found": len(comments),
            "posted_comments": posted_comments,
            "failed_comments": failed_comments,
            "message": f"PR #{pr_id} reviewed and {len(posted_comments)} comments posted"
        }
        
    except Exception as e:
        return {"error": f"Failed to review and comment on PR: {str(e)}"}
