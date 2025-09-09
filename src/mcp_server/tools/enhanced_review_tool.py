from typing import Dict, Any, List
from fastmcp import FastMCP
from services.bitbucket_service import BitbucketService
from services.sanitization_service import SanitizationService
from services.diff_parser_service import DiffParserService
from services.platform_detection_service import PlatformDetectionService
from models.comment import Comment, SeverityLevel


def register_enhanced_review_tool(mcp: FastMCP, bitbucket_service: BitbucketService, sanitization_service: SanitizationService):
    @mcp.tool()
    async def review_pr_with_line_comments(pr_id: str, repository: str) -> Dict[str, Any]:
        """
        Review a PR and prepare line-specific comments for posting. Skips P2 comments as requested.
        This tool analyzes the diff, finds specific issues, and prepares comments for the proper MCP workflow.
        Use 'preview_review_comments' and 'post_review_comments' to actually post the comments.
        """
        try:
            # Get PR details
            pr_details = await bitbucket_service.get_pr_details(pr_id, repository)
            
            # Get and sanitize diff
            diff = await bitbucket_service.get_pr_diff(pr_id, repository)
            sanitized_diff = sanitization_service.sanitize_diff(diff)
            
            # Parse diff to find specific issues
            diff_parser = DiffParserService()
            file_changes = diff_parser.get_file_changes(sanitized_diff)
            
            # Detect platform
            platform_detector = PlatformDetectionService()
            platform = platform_detector.detect_platform(repository)
            platform_checklist = platform_detector.get_platform_checklist(platform)
            
            # Analyze diff for specific issues
            comments = []
            
            # 1. Check for Swift-specific issues
            swift_issues = diff_parser.extract_swift_issues(sanitized_diff)
            for issue in swift_issues:
                if '!' in issue.content and issue.content.strip().endswith('!'):
                    comments.append({
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "content": "**P0 Issue:** Force unwrapping detected\n\nForce unwrapping (`!`) can cause runtime crashes. Consider using safe unwrapping with `if let` or `guard let` instead.",
                        "severity": "P0",
                        "is_summary": False
                    })
                elif 'print(' in issue.content or 'NSLog(' in issue.content:
                    comments.append({
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "content": "**P1 Issue:** Debug print statement\n\nConsider using proper logging instead of `print()` or `NSLog()` for production code.",
                        "severity": "P1",
                        "is_summary": False
                    })
                elif 'as!' in issue.content:
                    comments.append({
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "content": "**P1 Issue:** Force casting detected\n\nForce casting (`as!`) can cause runtime crashes. Consider using safe casting with `as?` instead.",
                        "severity": "P1",
                        "is_summary": False
                    })
            
            # 2. Check for extension function issues
            extension_issues = diff_parser.extract_extension_function_issues(sanitized_diff)
            for issue in extension_issues:
                if "isNotNullOrEmpty" in issue.content:
                    comments.append({
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "content": "**P0 Issue:** Redundant extension function\n\nThe function `isNotNullOrEmpty()` is redundant with Kotlin's built-in `isNullOrEmpty()`. Consider removing it or renaming to `isNotNullAndNotEmpty()` for clarity.",
                        "severity": "P0",
                        "is_summary": False
                    })
                elif 'isEmpty' in issue.content and 'if' in issue.content:
                    comments.append({
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "content": "**P1 Issue:** Empty string check\n\nConsider using `isEmpty` property directly instead of checking length. This is more idiomatic Swift code.",
                        "severity": "P1",
                        "is_summary": False
                    })
            
            # 3. Check for import issues
            import_issues = diff_parser.extract_import_issues(sanitized_diff)
            if import_issues:
                # Group by file
                import_files = {}
                for issue in import_issues:
                    if issue.file_path not in import_files:
                        import_files[issue.file_path] = []
                    import_files[issue.file_path].append(issue)
                
                for file_path, issues in import_files.items():
                    if len(issues) > 3:  # If many imports were changed
                        comments.append({
                            "file_path": file_path,
                            "line_number": issues[0].line_number,
                            "content": "**P1 Issue:** Import cleanup needed\n\nSeveral imports were modified. Verify all remaining imports are actually used. Run \"Optimize Imports\" in Xcode to clean up any remaining unused imports.",
                            "severity": "P1",
                            "is_summary": False
                        })
            
            # 4. Check for missing documentation
            doc_issues = diff_parser.extract_documentation_issues(sanitized_diff)
            if not doc_issues:
                # Look for complex functions without comments
                for file_path, changes in file_changes.items():
                    for change in changes:
                        if change.is_addition and ("func " in change.content or "class " in change.content or "struct " in change.content):
                            if not any("//" in c.content or "/*" in c.content for c in changes):
                                comments.append({
                                    "file_path": file_path,
                                    "line_number": change.line_number,
                                    "content": "**P1 Issue:** Missing documentation\n\nConsider adding documentation for this function/class to explain its purpose and usage.",
                                    "severity": "P1",
                                    "is_summary": False
                                })
                                break
            
            # No summary comment - only inline comments on specific code lines
            
            return {
                "success": True,
                "pr_id": pr_id,
                "repository": repository,
                "platform": platform.value,
                "total_issues_found": len(comments),
                "comments_prepared": len(comments),
                "comments": comments,
                "message": f"Prepared {len(comments)} inline comments for PR #{pr_id} in {repository}. Use 'preview_review_comments' to see them, then 'post_review_comments' with confirmation=true to post.",
                "next_steps": [
                    "Call 'preview_review_comments' to see the prepared comments",
                    "Call 'post_review_comments' with confirmation=true to post them"
                ]
            }
            
        except Exception as e:
            return {"error": f"Failed to review PR: {str(e)}"}

    @mcp.tool()
    async def analyze_diff_for_issues(pr_id: str, repository: str) -> Dict[str, Any]:
        """
        Analyze a PR diff and identify specific issues with line numbers and file paths.
        This is a helper tool to see what issues would be found before posting comments.
        """
        try:
            # Get and sanitize diff
            diff = await bitbucket_service.get_pr_diff(pr_id, repository)
            sanitized_diff = sanitization_service.sanitize_diff(diff)
            
            # Parse diff
            diff_parser = DiffParserService()
            file_changes = diff_parser.get_file_changes(sanitized_diff)
            
            # Find specific issues
            extension_issues = diff_parser.extract_extension_function_issues(sanitized_diff)
            import_issues = diff_parser.extract_import_issues(sanitized_diff)
            doc_issues = diff_parser.extract_documentation_issues(sanitized_diff)
            
            issues = []
            
            # Extension function issues
            for issue in extension_issues:
                if "isNotNullOrEmpty" in issue.content:
                    issues.append({
                        "type": "Extension Function",
                        "severity": "P0",
                        "file_path": issue.file_path,
                        "line_number": issue.line_number,
                        "content": issue.content,
                        "description": "Redundant extension function found"
                    })
            
            # Import issues
            import_files = {}
            for issue in import_issues:
                if issue.file_path not in import_files:
                    import_files[issue.file_path] = []
                import_files[issue.file_path].append(issue)
            
            for file_path, file_issues in import_files.items():
                if len(file_issues) > 3:
                    issues.append({
                        "type": "Import Cleanup",
                        "severity": "P1",
                        "file_path": file_path,
                        "line_number": file_issues[0].line_number,
                        "content": f"{len(file_issues)} import changes",
                        "description": "Multiple import changes detected"
                    })
            
            return {
                "pr_id": pr_id,
                "repository": repository,
                "total_issues": len(issues),
                "issues": issues,
                "file_changes": list(file_changes.keys()),
                "message": f"Found {len(issues)} issues in PR #{pr_id}"
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze diff: {str(e)}"}
