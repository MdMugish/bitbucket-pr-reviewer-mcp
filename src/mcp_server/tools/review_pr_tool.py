from typing import Dict, Any
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from services.matching_service import MatchingService
from services.sanitization_service import SanitizationService
from services.platform_detection_service import PlatformDetectionService


def register_review_pr_tool(mcp: FastMCP, bitbucket_service: BitbucketService, 
                          matching_service: MatchingService, sanitization_service: SanitizationService):
    @mcp.tool()
    async def review_pull_request(pr_identifier: str) -> Dict[str, Any]:
        try:
            # Check for multiple matches first
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
            sanitized_diff = await sanitization_service.sanitize_pr_diff(pr.id, pr.repository, bitbucket_service)
            
            # Detect platform and get platform-specific checklist
            platform_detector = PlatformDetectionService()
            platform = platform_detector.detect_platform(pr.repository)
            platform_checklist = platform_detector.get_platform_checklist(platform)
            
            return {
                "pr_id": pr.id,
                "title": pr.title,
                "author": pr.author,
                "status": pr.status,
                "repository": pr.repository,
                "sanitized_diff": sanitized_diff,
                "ready_for_review": True,
                "message": f"Ready to review PR: {pr.title} from {pr.repository}",
                "platform_detected": platform.value,
                "platform_checklist": platform_checklist,
                "review_instructions": {
                    "code_analysis": "Analyze the sanitized diff and identify specific code issues with exact line numbers and code snippets",
                    "platform_specific_review": f"Use the {platform_checklist['platform']} checklist below to ensure comprehensive review",
                    "severity_levels": {
                        "P0": "Critical issues that must be fixed (security, data loss, crashes)",
                        "P1": "Important issues that should be fixed (performance, maintainability)",
                        "P2": "Minor issues or suggestions (code style, documentation)"
                    },
                    "required_output": [
                        "Show actual code snippets where issues are found",
                        "Categorize each issue by severity (P0/P1/P2)",
                        "Provide specific line-by-line feedback",
                        f"Check against {platform_checklist['platform']} specific requirements",
                        "After review, automatically offer to post comments on the PR"
                    ]
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to prepare PR for review: {str(e)}"}
