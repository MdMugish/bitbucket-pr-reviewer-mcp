import os
import sys
from typing import Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class BitbucketConfig(BaseModel):
    username: str
    app_password: str
    workspace: str
    repositories: list[str]


class ReviewConfig(BaseModel):
    severity_levels: Dict[str, str]
    comment_template: str
    max_comments_per_pr: int
    fuzzy_match_threshold: int


class SanitizationConfig(BaseModel):
    patterns: list[str]
    replacement: str
    preserve_structure: bool


class Settings(BaseModel):
    bitbucket: BitbucketConfig
    review: ReviewConfig
    sanitization: SanitizationConfig
    log_level: str = "INFO"


def load_settings() -> Settings:
    # Parse comma-separated repositories for backward compatibility
    repos_str = os.getenv("BITBUCKET_REPOSITORIES", "")
    if not repos_str:
        # Fallback to single repository for backward compatibility
        single_repo = os.getenv("BITBUCKET_REPOSITORY", "")
        repositories = [single_repo] if single_repo else []
    else:
        repositories = [repo.strip() for repo in repos_str.split(",") if repo.strip()]
    
    # Validate required environment variables
    username = os.getenv("BITBUCKET_USERNAME", "")
    app_password = os.getenv("BITBUCKET_APP_PASSWORD", "")
    workspace = os.getenv("BITBUCKET_WORKSPACE", "")
    
    # Only show warnings if we're in debug mode or if critical settings are missing
    debug_mode = os.getenv("DEBUG", "").lower() in ("true", "1", "yes")
    
    if not username and debug_mode:
        print("Warning: BITBUCKET_USERNAME not set", file=sys.stderr)
    if not app_password and debug_mode:
        print("Warning: BITBUCKET_APP_PASSWORD not set", file=sys.stderr)
    if not workspace and debug_mode:
        print("Warning: BITBUCKET_WORKSPACE not set", file=sys.stderr)
    if not repositories and debug_mode:
        print("Warning: No repositories configured (BITBUCKET_REPOSITORIES or BITBUCKET_REPOSITORY)", file=sys.stderr)
    
    return Settings(
        bitbucket=BitbucketConfig(
            username=username,
            app_password=app_password,
            workspace=workspace,
            repositories=repositories
        ),
        review=ReviewConfig(
            severity_levels={
                "P0": "Critical security or functionality issues",
                "P1": "Code quality improvements",
                "P2": "Minor warnings and suggestions"
            },
            comment_template="[AI - Review] {severity}: {message}",
            max_comments_per_pr=20,
            fuzzy_match_threshold=80
        ),
        sanitization=SanitizationConfig(
            patterns=[
                # Common credential patterns - capture only the credential part
                r"(password\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(api_key\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(token\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(secret\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(key\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(auth\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(pass\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                r"(pwd\s*[:=]\s*['\"])([^'\"]*)(['\"])",
                
                # Environment variable patterns - capture only the value
                r"(export\s+\w*PASSWORD\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(export\s+\w*SECRET\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(export\s+\w*KEY\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(export\s+\w*TOKEN\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(export\s+\w*AUTH\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(\w*PASSWORD\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(\w*SECRET\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(\w*KEY\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(\w*TOKEN\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                r"(\w*AUTH\w*\s*=\s*['\"])([^'\"]*)(['\"])",
                
                # API keys and tokens (various formats) - capture only the key
                r"(sk-[a-zA-Z0-9]{20,})",
                r"(sk-proj-[a-zA-Z0-9]{20,})",
                r"(pk_[a-zA-Z0-9]{20,})",
                r"(pk_test_[a-zA-Z0-9]{20,})",
                r"(xoxb-[a-zA-Z0-9-]+)",
                r"(xoxp-[a-zA-Z0-9-]+)",
                r"(ghp_[a-zA-Z0-9]{36,})",
                r"(gho_[a-zA-Z0-9]{36,})",
                r"(ghu_[a-zA-Z0-9]{36,})",
                r"(ghs_[a-zA-Z0-9]{36,})",
                r"(ghr_[a-zA-Z0-9]{36,})",
                
                # Database credentials - capture only the password part
                r"(mongodb://[^:]+:)([^@]+)(@)",
                r"(postgres://[^:]+:)([^@]+)(@)",
                r"(mysql://[^:]+:)([^@]+)(@)",
                r"(redis://[^:]+:)([^@]+)(@)",
                
                # AWS credentials - capture only the key
                r"(AKIA[0-9A-Z]{16})",
                # Removed generic 40-char pattern that was matching file paths
                
                # JWT tokens - capture only the token
                r"(eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)",
                
                # Generic patterns - capture only the credential (but not file paths)
                # Made more specific to avoid matching file paths
                r"(password\s*[:=]\s*['\"])([a-zA-Z0-9+/]{20,})(['\"])",  # Long base64-like passwords
                r"(secret\s*[:=]\s*['\"])([a-f0-9]{32,})(['\"])",         # Long hex secrets
                r"(key\s*[:=]\s*['\"])([a-zA-Z0-9_]{8,})(['\"])",        # Medium length keys
            ],
            replacement="[REDACTED]",
            preserve_structure=True
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO")
    )
