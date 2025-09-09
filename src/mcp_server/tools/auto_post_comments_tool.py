from typing import Dict, Any, List
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from services.platform_detection_service import PlatformDetectionService


def register_auto_post_comments_tool(mcp: FastMCP, bitbucket_service: BitbucketService):
    @mcp.tool()
    async def auto_post_review_comments(pr_id: str, repository: str, review_feedback: str) -> Dict[str, Any]:
        """
        Automatically parse review feedback and offer to post structured comments on the PR.
        This tool should be called after a PR review is completed to offer posting comments.
        """
        try:
            # Detect platform for context
            platform_detector = PlatformDetectionService()
            platform = platform_detector.detect_platform(repository)
            platform_checklist = platform_detector.get_platform_checklist(platform)
            
            # Parse the review feedback to extract issues with severity levels
            issues = _parse_review_feedback(review_feedback)
            
            if not issues:
                return {
                    "message": "No specific issues found in the review feedback to post as comments.",
                    "suggestion": "Review feedback should contain specific code issues with P0/P1/P2 severity levels.",
                    "platform_detected": platform.value,
                    "platform_checklist": platform_checklist
                }
            
            # Group issues by severity
            p0_issues = [issue for issue in issues if issue.get("severity") == "P0"]
            p1_issues = [issue for issue in issues if issue.get("severity") == "P1"]
            p2_issues = [issue for issue in issues if issue.get("severity") == "P2"]
            
            # Create structured comments
            comments = []
            
            # Add individual issue comments
            for issue in issues:
                comment = {
                    "file_path": issue.get("file_path", "Unknown"),
                    "line_number": issue.get("line_number", 0),
                    "content": f"**{issue['severity']} Issue:** {issue['title']}\n\n"
                              f"**Code:**\n```\n{issue.get('code_snippet', 'N/A')}\n```\n\n"
                              f"**Issue:** {issue['description']}\n\n"
                              f"**Suggestion:** {issue.get('suggestion', 'Please review and fix.')}",
                    "severity": issue["severity"]
                }
                comments.append(comment)
            
            # Add summary comment
            summary_comment = {
                "file_path": None,  # Summary comment
                "line_number": None,
                "content": f"**PR Review Summary**\n\n"
                          f"**Total Issues Found:** {len(issues)}\n"
                          f"• **P0 (Critical):** {len(p0_issues)} issues\n"
                          f"• **P1 (Important):** {len(p1_issues)} issues\n"
                          f"• **P2 (Minor):** {len(p2_issues)} issues\n\n"
                          f"**Review completed by AI.** Please address P0 issues immediately, "
                          f"consider P1 issues for next iteration, and P2 issues when convenient.",
                "severity": "SUMMARY"
            }
            comments.append(summary_comment)
            
            return {
                "pr_id": pr_id,
                "repository": repository,
                "platform_detected": platform.value,
                "platform_checklist": platform_checklist,
                "comments_ready": True,
                "total_comments": len(comments),
                "severity_breakdown": {
                    "P0": len(p0_issues),
                    "P1": len(p1_issues),
                    "P2": len(p2_issues)
                },
                "comments": comments,
                "message": f"Ready to post {len(comments)} comments on PR #{pr_id} for {platform_checklist['platform']}",
                "next_step": "Use 'preview_review_comments' to see the comments, then 'post_review_comments' to post them."
            }
            
        except Exception as e:
            return {"error": f"Failed to parse review feedback: {str(e)}"}


def _parse_review_feedback(feedback: str) -> List[Dict[str, Any]]:
    """
    Parse review feedback to extract structured issues.
    This is a basic parser - in a real implementation, you might want to use NLP or structured prompts.
    """
    issues = []
    lines = feedback.split('\n')
    
    current_issue = None
    current_code = []
    in_code_block = False
    
    for line in lines:
        line = line.strip()
        
        # Detect severity markers
        if line.startswith('**P0') or 'P0:' in line or 'P0 ' in line:
            if current_issue:
                issues.append(current_issue)
            current_issue = {
                "severity": "P0",
                "title": "Critical Issue",
                "description": line,
                "code_snippet": "",
                "file_path": "Unknown",
                "line_number": 0
            }
        elif line.startswith('**P1') or 'P1:' in line or 'P1 ' in line:
            if current_issue:
                issues.append(current_issue)
            current_issue = {
                "severity": "P1",
                "title": "Important Issue",
                "description": line,
                "code_snippet": "",
                "file_path": "Unknown",
                "line_number": 0
            }
        elif line.startswith('**P2') or 'P2:' in line or 'P2 ' in line:
            if current_issue:
                issues.append(current_issue)
            current_issue = {
                "severity": "P2",
                "title": "Minor Issue",
                "description": line,
                "code_snippet": "",
                "file_path": "Unknown",
                "line_number": 0
            }
        
        # Detect code blocks
        elif line.startswith('```'):
            in_code_block = not in_code_block
            if not in_code_block and current_issue:
                current_issue["code_snippet"] = '\n'.join(current_code)
                current_code = []
        elif in_code_block:
            current_code.append(line)
        
        # Update current issue description
        elif current_issue and not in_code_block:
            if current_issue["description"] == line:
                continue  # Skip the severity line itself
            current_issue["description"] += f" {line}"
    
    # Add the last issue
    if current_issue:
        issues.append(current_issue)
    
    return issues
