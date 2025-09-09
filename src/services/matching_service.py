from typing import Optional, List
from fuzzywuzzy import fuzz
from models.pull_request import PullRequest
from services.bitbucket_service import BitbucketService


class MatchingService:
    def __init__(self):
        self.threshold = 80

    async def find_pr(self, identifier: str, bitbucket_service: BitbucketService) -> Optional[PullRequest]:
        prs = await bitbucket_service.get_all_pull_requests()
        
        exact_matches = self._find_exact_matches(identifier, prs)
        if len(exact_matches) == 1:
            return exact_matches[0]
        elif len(exact_matches) > 1:
            return None  # Multiple exact matches - need user confirmation
        
        fuzzy_matches = self._find_fuzzy_matches(identifier, prs)
        if len(fuzzy_matches) == 1:
            return fuzzy_matches[0]
        elif len(fuzzy_matches) > 1:
            return None  # Multiple fuzzy matches - need user confirmation
            
        return None
    
    async def find_multiple_prs(self, identifier: str, bitbucket_service: BitbucketService) -> List[PullRequest]:
        prs = await bitbucket_service.get_all_pull_requests()
        
        exact_matches = self._find_exact_matches(identifier, prs)
        if exact_matches:
            return exact_matches
        
        fuzzy_matches = self._find_fuzzy_matches(identifier, prs)
        return fuzzy_matches

    def _find_exact_matches(self, identifier: str, prs: List[PullRequest]) -> List[PullRequest]:
        identifier_lower = identifier.lower()
        matches = []
        
        for pr in prs:
            if (identifier_lower == pr.title.lower() or 
                identifier_lower == pr.id.lower() or
                identifier_lower in pr.title.lower()):
                matches.append(pr)
        
        return matches

    def _find_fuzzy_matches(self, identifier: str, prs: List[PullRequest]) -> List[PullRequest]:
        matches = []
        
        for pr in prs:
            title_score = fuzz.ratio(identifier.lower(), pr.title.lower())
            if title_score >= self.threshold:
                matches.append(pr)
        
        return sorted(matches, key=lambda x: fuzz.ratio(identifier.lower(), x.title.lower()), reverse=True)
