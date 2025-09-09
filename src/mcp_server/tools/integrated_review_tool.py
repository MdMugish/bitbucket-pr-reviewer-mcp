from typing import Dict, Any, List
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from services.platform_detection_service import PlatformDetectionService
from services.sanitization_service import SanitizationService
from services.matching_service import MatchingService
from services.diff_parser_service import DiffParserService
from models.comment import Comment, SeverityLevel


def register_integrated_review_tool(mcp: FastMCP, bitbucket_service: BitbucketService, sanitization_service: SanitizationService):
    diff_parser = DiffParserService()
    @mcp.tool()
    async def review_and_preview_comments(pr_identifier: str) -> Dict[str, Any]:
        """
        Complete PR review workflow: Find PR, analyze, and prepare comments for preview.
        This tool handles the entire review process and prepares comments for user confirmation.
        """
        try:
            # Find the PR
            matching_service = MatchingService()
            prs = await bitbucket_service.get_all_pull_requests()
            matching_prs = matching_service.find_multiple_prs(prs, pr_identifier)
            
            if not matching_prs:
                return {
                    "error": "PR not found",
                    "message": f"No PR found matching '{pr_identifier}'",
                    "suggestion": "Try 'Review PR' to see all available PRs"
                }
            
            if len(matching_prs) > 1:
                return {
                    "multiple_matches": True,
                    "message": f"Found {len(matching_prs)} PRs matching '{pr_identifier}'",
                    "options": [
                        {
                            "pr_id": pr.id,
                            "title": pr.title,
                            "repository": pr.repository,
                            "author": pr.author
                        } for pr in matching_prs
                    ],
                    "suggestion": "Please specify which PR you want to review"
                }
            
            # Get the specific PR
            pr = matching_prs[0]
            
            # Detect platform
            platform_detector = PlatformDetectionService()
            platform = platform_detector.detect_platform(pr.repository)
            platform_checklist = platform_detector.get_platform_checklist(platform)
            
            # Get sanitized diff
            sanitized_diff = await sanitization_service.sanitize_pr_diff(pr.id, pr.repository, bitbucket_service)
            
            # Create review instructions for the AI
            review_instructions = f"""
You are reviewing a {platform_checklist['platform']} pull request. Please analyze the code and provide specific feedback.

PR Details:
- Title: {pr.title}
- Repository: {pr.repository}
- Author: {pr.author}
- Platform: {platform_checklist['platform']}

Code Changes:
```diff
{sanitized_diff}
```

Platform-Specific Checklist:
{platform_checklist['checklist']}

Please provide a detailed review with:
1. Specific code issues found (with line numbers if possible)
2. Severity level for each issue (P0=Critical, P1=Important, P2=Minor)
3. Code snippets showing the problematic areas
4. Specific suggestions for improvement
5. Overall summary

Format your response with clear P0/P1/P2 markers for each issue.
"""
            
            # Prepare the response for AI analysis
            return {
                "pr_id": pr.id,
                "title": pr.title,
                "repository": pr.repository,
                "author": pr.author,
                "platform_detected": platform.value,
                "platform_checklist": platform_checklist,
                "sanitized_diff": sanitized_diff,
                "review_instructions": review_instructions,
                "message": f"PR '{pr.title}' is ready for AI review. The AI will analyze the code and provide structured feedback.",
                "next_step": "The AI will now analyze this PR and provide detailed feedback with specific issues and suggestions.",
                "ready_for_ai_analysis": True
            }
            
        except Exception as e:
            return {"error": f"Failed to prepare PR for review: {str(e)}"}
    
    @mcp.tool()
    async def parse_ai_feedback_with_line_numbers(pr_id: str, repository: str, ai_feedback: str) -> Dict[str, Any]:
        """
        Parse AI feedback and map it to actual file paths and line numbers from the diff.
        This tool takes AI feedback and creates properly structured comments with correct file paths and line numbers.
        """
        try:
            # Get the actual diff to parse file paths and line numbers
            diff = await bitbucket_service.get_pr_diff(pr_id, repository)
            if not diff:
                return {
                    "error": "Failed to get PR diff",
                    "message": "Could not retrieve the diff for this PR"
                }
            
            # Parse the diff to get file locations
            diff_locations = diff_parser.parse_diff(diff)
            
            # Parse the AI feedback to extract issues
            issues = _parse_review_feedback(ai_feedback)
            
            if not issues:
                return {
                    "error": "No issues found",
                    "message": "Could not parse any issues from the AI feedback"
                }
            
            # Map issues to actual file locations
            structured_comments = []
            
            for issue in issues:
                # Try to find matching file location based on code snippet or description
                matched_location = None
                
                # Look for file references in the description
                description = issue["description"]
                
                # Extract file names from the description
                import re
                file_matches = re.findall(r'(\w+\.swift)', description)
                file_matches.extend(re.findall(r'(\w+\.pbxproj)', description))
                
                # Try to find matching locations
                for file_name in file_matches:
                    for location in diff_locations:
                        if file_name in location.file_path:
                            matched_location = location
                            break
                    if matched_location:
                        break
                
                # If no file match found, try to match by content
                if not matched_location and issue.get("code_snippet"):
                    for location in diff_locations:
                        if issue["code_snippet"].strip() in location.content:
                            matched_location = location
                            break
                
                # Create structured comment
                comment = {
                    "content": issue["description"],
                    "severity": issue["severity"],
                    "file_path": matched_location.file_path if matched_location else "Unknown",
                    "line_number": matched_location.line_number if matched_location else 0,
                    "is_summary": False
                }
                
                structured_comments.append(comment)
            
            return {
                "success": True,
                "pr_id": pr_id,
                "repository": repository,
                "comments": structured_comments,
                "message": f"Parsed {len(structured_comments)} comments with file paths and line numbers",
                "next_step": "Use 'post_review_comments' with confirmation=true to post these comments"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to parse AI feedback: {str(e)}",
                "message": "Could not process the AI feedback and map it to file locations"
            }

    @mcp.tool()
    async def parse_and_preview_comments(pr_id: str, repository: str, ai_review_feedback: str) -> Dict[str, Any]:
        """
        Parse AI review feedback and create a preview of comments to be posted.
        This shows exactly what will be posted before asking for confirmation.
        """
        try:
            # Parse the AI feedback to extract structured issues
            issues = _parse_ai_feedback(ai_review_feedback)
            
            if not issues:
                return {
                    "message": "No specific issues found in the AI review feedback.",
                    "suggestion": "The AI review should contain specific code issues with P0/P1/P2 severity levels.",
                    "pr_id": pr_id,
                    "repository": repository
                }
            
            # Create structured comments
            comments = []
            
            # Add individual issue comments
            for issue in issues:
                comment = {
                    "file_path": issue.get("file_path", "Unknown"),
                    "line_number": issue.get("line_number"),
                    "content": f"**{issue['severity']} Issue:** {issue['title']}\n\n"
                              f"**Code:**\n```\n{issue.get('code_snippet', 'N/A')}\n```\n\n"
                              f"**Issue:** {issue['description']}\n\n"
                              f"**Suggestion:** {issue.get('suggestion', 'Please review and fix.')}",
                    "severity": issue["severity"],
                    "is_summary": False
                }
                comments.append(comment)
            
            # Add summary comment
            p0_count = len([i for i in issues if i.get("severity") == "P0"])
            p1_count = len([i for i in issues if i.get("severity") == "P1"])
            p2_count = len([i for i in issues if i.get("severity") == "P2"])
            
            summary_comment = {
                "file_path": None,
                "line_number": None,
                "content": f"**PR Review Summary**\n\n"
                          f"**Total Issues Found:** {len(issues)}\n"
                          f"• **P0 (Critical):** {p0_count} issues\n"
                          f"• **P1 (Important):** {p1_count} issues\n"
                          f"• **P2 (Minor):** {p2_count} issues\n\n"
                          f"**Review completed by AI.** Please address P0 issues immediately, "
                          f"consider P1 issues for next iteration, and P2 issues when convenient.",
                "severity": "SUMMARY",
                "is_summary": True
            }
            comments.append(summary_comment)
            
            # Create preview with formatted comments
            preview_comments = []
            for comment in comments:
                formatted_comment = f"[AI - Review] {comment['severity']}: {comment['content']}"
                preview_comments.append({
                    "severity": comment["severity"],
                    "content": comment["content"],
                    "formatted": formatted_comment,
                    "file_path": comment["file_path"],
                    "line_number": comment["line_number"],
                    "is_summary": comment["is_summary"]
                })
            
            return {
                "pr_id": pr_id,
                "repository": repository,
                "total_comments": len(comments),
                "severity_breakdown": {
                    "P0 (Critical)": p0_count,
                    "P1 (Important)": p1_count,
                    "P2 (Minor)": p2_count,
                    "Summary": 1
                },
                "comments_preview": preview_comments,
                "message": f"Ready to post {len(comments)} comments to PR #{pr_id} in {repository}",
                "requires_confirmation": True,
                "confirmation_instruction": "Review the comments above. If you want to post them, use 'post_review_comments' with confirmation=true"
            }
            
        except Exception as e:
            return {"error": f"Failed to parse AI feedback: {str(e)}"}


def _parse_ai_feedback(feedback: str) -> List[Dict[str, Any]]:
    """
    Parse AI review feedback to extract structured issues.
    Looks for P0/P1/P2 markers and extracts relevant information.
    """
    issues = []
    lines = feedback.split('\n')
    
    current_issue = None
    current_code = []
    in_code_block = False
    
    for line in lines:
        line = line.strip()
        
        # Detect severity markers
        if any(marker in line for marker in ['**P0**', 'P0:', 'P0 ', 'P0-']):
            if current_issue:
                issues.append(current_issue)
            current_issue = {
                "severity": "P0",
                "title": "Critical Issue",
                "description": line,
                "code_snippet": "",
                "file_path": None,
                "line_number": None
            }
        elif any(marker in line for marker in ['**P1**', 'P1:', 'P1 ', 'P1-']):
            if current_issue:
                issues.append(current_issue)
            current_issue = {
                "severity": "P1",
                "title": "Important Issue", 
                "description": line,
                "code_snippet": "",
                "file_path": None,
                "line_number": None
            }
        elif any(marker in line for marker in ['**P2**', 'P2:', 'P2 ', 'P2-']):
            if current_issue:
                issues.append(current_issue)
            current_issue = {
                "severity": "P2",
                "title": "Minor Issue",
                "description": line,
                "code_snippet": "",
                "file_path": None,
                "line_number": None
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
        elif current_issue and not in_code_block and line:
            if current_issue["description"] != line:
                current_issue["description"] += f" {line}"
    
    # Add the last issue
    if current_issue:
        issues.append(current_issue)
    
    return issues
