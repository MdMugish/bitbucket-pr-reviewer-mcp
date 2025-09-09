from typing import List, Dict, Any
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from models.comment import Comment, SeverityLevel


def register_post_comments_tool(mcp: FastMCP, bitbucket_service: BitbucketService):
    @mcp.tool()
    async def preview_review_comments(pr_id: str, repository: str, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Preview comments before posting them to the PR. Shows a summary and asks for confirmation."""
        try:
            comment_objects = []
            for comment_data in comments:
                comment = Comment(
                    content=comment_data["content"],
                    severity=SeverityLevel(comment_data["severity"]),
                    line_number=comment_data.get("line_number"),
                    file_path=comment_data.get("file_path"),
                    is_summary=comment_data.get("is_summary", False)
                )
                comment_objects.append(comment)
            
            # Group comments by severity
            severity_groups = {"P0": [], "P1": [], "P2": []}
            summary_comments = []
            
            for comment in comment_objects:
                if comment.is_summary:
                    summary_comments.append(comment)
                else:
                    severity_groups[comment.severity.value].append(comment)
            
            # Create preview summary
            preview_summary = {
                "pr_id": pr_id,
                "repository": repository,
                "total_comments": len(comment_objects),
                "severity_breakdown": {
                    "P0 (Critical)": len(severity_groups["P0"]),
                    "P1 (Important)": len(severity_groups["P1"]),
                    "P2 (Warning)": len(severity_groups["P2"]),
                    "Summary": len(summary_comments)
                },
                "comments_preview": []
            }
            
            # Add preview for each comment
            for comment in comment_objects:
                preview_item = {
                    "severity": comment.severity.value,
                    "content": comment.content,
                    "file_path": comment.file_path,
                    "line_number": comment.line_number,
                    "is_summary": comment.is_summary,
                    "formatted": f"[AI - Review] {comment.severity.value}: {comment.content}"
                }
                preview_summary["comments_preview"].append(preview_item)
            
            preview_summary["message"] = f"Ready to post {len(comment_objects)} comments to PR {pr_id} in {repository}. Use 'post_review_comments' with confirmation=true to proceed."
            preview_summary["requires_confirmation"] = True
            
            return preview_summary
            
        except Exception as e:
            return {"error": f"Failed to preview comments: {str(e)}"}

    @mcp.tool()
    async def post_review_comments(pr_id: str, repository: str, comments: List[Dict[str, Any]], confirmation: bool = False) -> Dict[str, Any]:
        """Post comments to the PR. Requires confirmation=true to proceed."""
        try:
            if not confirmation:
                return {
                    "error": "Confirmation required",
                    "message": "You must set confirmation=true to post comments. Use 'preview_review_comments' first to see what will be posted.",
                    "suggestion": "Call preview_review_comments first, then post_review_comments with confirmation=true"
                }
            
            comment_objects = []
            for comment_data in comments:
                comment = Comment(
                    content=comment_data["content"],
                    severity=SeverityLevel(comment_data["severity"]),
                    line_number=comment_data.get("line_number"),
                    file_path=comment_data.get("file_path"),
                    is_summary=comment_data.get("is_summary", False)
                )
                comment_objects.append(comment)
            
            posted_comments = []
            failed_comments = []
            
            for comment in comment_objects:
                try:
                    # Skip P2 comments as requested
                    if comment.severity.value == "P2":
                        print(f"Skipping P2 comment: {comment.content[:50]}...")
                        continue
                    
                    # Skip summary comments - only post inline comments on specific code lines
                    if comment.is_summary or comment.severity.value == "SUMMARY":
                        print(f"Skipping summary comment: {comment.content[:50]}...")
                        continue
                    
                    # Ensure comment content doesn't already have the prefix
                    content = comment.content
                    if not content.startswith("[AI - Review]"):
                        formatted_comment = f"[AI - Review] {comment.severity.value}: {content}"
                    else:
                        formatted_comment = content
                    
                    # Post comment with file path if available
                    success = await bitbucket_service.post_comment(
                        pr_id, 
                        repository, 
                        formatted_comment, 
                        comment.line_number,
                        comment.file_path
                    )
                    if success:
                        posted_comments.append({
                            "severity": comment.severity.value,
                            "content": comment.content[:100] + "..." if len(comment.content) > 100 else comment.content,
                            "line_number": comment.line_number
                        })
                    else:
                        failed_comments.append({
                            "severity": comment.severity.value,
                            "error": "Failed to post comment"
                        })
                except Exception as e:
                    error_msg = str(e)
                    if "line_form" in error_msg:
                        error_msg = "API parameter error - this has been fixed in the latest version"
                    elif "401" in error_msg:
                        error_msg = "Authentication failed - check Bitbucket credentials"
                    elif "403" in error_msg:
                        error_msg = "Permission denied - check repository access"
                    elif "404" in error_msg:
                        error_msg = "PR not found - check PR ID and repository"
                    
                    failed_comments.append({
                        "severity": comment.severity.value,
                        "error": error_msg
                    })
            
            return {
                "success": len(failed_comments) == 0,
                "pr_id": pr_id,
                "repository": repository,
                "comments_posted": len(posted_comments),
                "comments_failed": len(failed_comments),
                "posted_comments": posted_comments,
                "failed_comments": failed_comments,
                "message": f"Posted {len(posted_comments)}/{len(comment_objects)} comments to PR {pr_id} in {repository}" +
                          (f". {len(failed_comments)} comments failed to post." if failed_comments else ""),
                "debug_info": {
                    "total_comments_attempted": len(comment_objects),
                    "successful_posts": len(posted_comments),
                    "failed_posts": len(failed_comments),
                    "api_endpoint": f"https://api.bitbucket.org/2.0/repositories/{repository}/pullrequests/{pr_id}/comments"
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to post comments: {str(e)}"}
