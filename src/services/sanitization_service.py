import re
from typing import List
from config.settings import Settings


class SanitizationService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.patterns = [re.compile(pattern) for pattern in settings.sanitization.patterns]

    async def sanitize_pr_diff(self, pr_id: str, repository: str, bitbucket_service) -> str:
        diff = await bitbucket_service.get_pr_diff(pr_id, repository)
        return self.sanitize_diff(diff)

    def sanitize_diff(self, diff: str) -> str:
        if diff is None:
            return ""
        
        sanitized = diff
        
        for pattern in self.patterns:
            # Handle different pattern types
            if pattern.groups == 3:  # Pattern with 3 capture groups (prefix, credential, suffix)
                sanitized = pattern.sub(r'\1[REDACTED]\3', sanitized)
            elif pattern.groups == 1:  # Pattern with 1 capture group (just the credential)
                sanitized = pattern.sub('[REDACTED]', sanitized)
            else:  # Fallback to simple replacement
                sanitized = pattern.sub(self.settings.sanitization.replacement, sanitized)
        
        return sanitized

    def detect_credentials(self, text: str) -> List[str]:
        found_credentials = []
        
        for pattern in self.patterns:
            matches = pattern.findall(text)
            if pattern.groups == 3:  # Pattern with 3 capture groups
                # Extract the credential part (group 2)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        found_credentials.append(match[1])
            elif pattern.groups == 1:  # Pattern with 1 capture group
                # The match is the credential itself
                found_credentials.extend(matches)
            else:
                # Fallback to full matches
                found_credentials.extend(matches)
        
        return found_credentials
