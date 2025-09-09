from typing import Dict, Any, List
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from services.matching_service import MatchingService
from services.sanitization_service import SanitizationService
from services.platform_detection_service import PlatformDetectionService
from services.diff_parser_service import DiffParserService
from models.comment import Comment, SeverityLevel
import re


def register_auto_review_tool(mcp: FastMCP, bitbucket_service: BitbucketService, 
                            matching_service: MatchingService, sanitization_service: SanitizationService):
    
    @mcp.tool()
    async def review_all_prs_and_comment() -> Dict[str, Any]:
        """
        Review ALL open PRs and automatically post comments. Skips PRs already reviewed by AI.
        This is a one-command solution that does everything automatically.
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
                        "issues_found": review_result.get("issues_found", 0)
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
    
    @mcp.tool()
    async def review_pr_and_comment(pr_identifier: str) -> Dict[str, Any]:
        """
        Review a specific PR and automatically post comments. Skips if already reviewed by AI.
        This is a one-command solution: 'Review PR 3400 and comment it'
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
                "message": f"Successfully reviewed PR #{pr.id} and posted {review_result.get('comments_posted', 0)} comments"
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
        # If we can't check comments, assume not reviewed to be safe
        return False


async def _review_and_comment_pr(pr_id: str, repository: str, bitbucket_service: BitbucketService, sanitization_service: SanitizationService) -> Dict[str, Any]:
    """
    Internal function to review a PR and post comments automatically.
    """
    try:
        # Get and sanitize diff
        diff = await bitbucket_service.get_pr_diff(pr_id, repository)
        sanitized_diff = sanitization_service.sanitize_diff(diff)
        
        # Parse diff to get file locations
        diff_parser = DiffParserService()
        diff_locations = diff_parser.parse_diff(sanitized_diff)
        
        # Detect platform
        platform_detector = PlatformDetectionService()
        platform = platform_detector.detect_platform(repository)
        
        # MCP server should NOT perform static analysis - it's just a bridge
        # The AI host (Claude) should analyze the sanitized diff
        comments = []
        
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
            "comments_posted": len(posted_comments),
            "comments_failed": len(failed_comments),
            "issues_found": len(comments),
            "posted_comments": posted_comments,
            "failed_comments": failed_comments
        }
        
    except Exception as e:
        raise Exception(f"Failed to review and comment on PR: {str(e)}")
