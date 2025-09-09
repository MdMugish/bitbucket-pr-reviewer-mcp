import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DiffLocation:
    file_path: str
    line_number: int
    content: str
    is_addition: bool  # True for + lines, False for - lines


class DiffParserService:
    """Service to parse git diffs and extract file paths, line numbers, and content."""
    
    def __init__(self):
        # Handle both normal and sanitized diffs
        self.file_header_pattern = re.compile(r'^diff --git a(?:\[REDACTED\])?/(.+?) b(?:\[REDACTED\])?/(.+?)$')
        self.hunk_header_pattern = re.compile(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@')
        self.addition_pattern = re.compile(r'^\+')
        self.removal_pattern = re.compile(r'^-')
    
    def parse_diff(self, diff: str) -> List[DiffLocation]:
        """Parse a git diff and return list of DiffLocation objects."""
        if not diff:
            return []
        
        locations = []
        lines = diff.split('\n')
        current_file = None
        current_line_number = None
        lines_since_hunk = 0
        
        for i, line in enumerate(lines):
            # Check for file header
            file_match = self.file_header_pattern.match(line)
            if file_match:
                current_file = file_match.group(2)  # Use the 'b' path (new file)
                current_line_number = None
                lines_since_hunk = 0
                continue
            
            # Check for hunk header
            hunk_match = self.hunk_header_pattern.match(line)
            if hunk_match:
                current_line_number = int(hunk_match.group(2))  # Start line in new file
                lines_since_hunk = 0
                continue
            
            # Skip if we don't have file context yet
            if not current_file or current_line_number is None:
                continue
            
            # Check for addition lines
            if self.addition_pattern.match(line):
                content = line[1:]  # Remove the + prefix
                actual_line_number = current_line_number + lines_since_hunk
                locations.append(DiffLocation(
                    file_path=current_file,
                    line_number=actual_line_number,
                    content=content,
                    is_addition=True
                ))
                lines_since_hunk += 1
            elif self.removal_pattern.match(line):
                # Don't increment line number for removals
                continue
            elif line.startswith(' '):
                # Context line - increment line number
                lines_since_hunk += 1
        
        return locations
    
    def parse_original_diff(self, diff: str) -> List[DiffLocation]:
        """Parse an original (unsanitized) git diff to get correct file paths for API calls."""
        if not diff:
            return []
        
        locations = []
        lines = diff.split('\n')
        current_file = None
        current_line_number = None
        lines_since_hunk = 0
        
        # Use pattern for original diffs (without [REDACTED])
        original_file_header_pattern = re.compile(r'^diff --git a/(.+?) b/(.+?)$')
        
        for i, line in enumerate(lines):
            # Check for file header
            file_match = original_file_header_pattern.match(line)
            if file_match:
                current_file = file_match.group(2)  # Use the 'b' path (new file)
                current_line_number = None
                lines_since_hunk = 0
                continue
            
            # Check for hunk header
            hunk_match = self.hunk_header_pattern.match(line)
            if hunk_match:
                current_line_number = int(hunk_match.group(2))  # Start line in new file
                lines_since_hunk = 0
                continue
            
            # Skip if we don't have file context yet
            if not current_file or current_line_number is None:
                continue
            
            # Check for addition lines
            if self.addition_pattern.match(line):
                content = line[1:]  # Remove the + prefix
                actual_line_number = current_line_number + lines_since_hunk
                locations.append(DiffLocation(
                    file_path=current_file,
                    line_number=actual_line_number,
                    content=content,
                    is_addition=True
                ))
                lines_since_hunk += 1
            elif self.removal_pattern.match(line):
                # Don't increment line number for removals
                continue
            elif line.startswith(' '):
                # Context line - increment line number
                lines_since_hunk += 1
        
        return locations
    
    def find_issue_locations(self, diff: str, issue_patterns: List[str]) -> List[DiffLocation]:
        """Find specific patterns in the diff and return their locations."""
        locations = self.parse_diff(diff)
        issue_locations = []
        
        for location in locations:
            for pattern in issue_patterns:
                if re.search(pattern, location.content, re.IGNORECASE):
                    issue_locations.append(location)
                    break
        
        return issue_locations
    
    def get_file_changes(self, diff: str) -> Dict[str, List[DiffLocation]]:
        """Group diff locations by file path."""
        locations = self.parse_diff(diff)
        file_changes = {}
        
        for location in locations:
            if location.file_path not in file_changes:
                file_changes[location.file_path] = []
            file_changes[location.file_path].append(location)
        
        return file_changes
    
    def extract_extension_function_issues(self, diff: str) -> List[DiffLocation]:
        """Extract issues related to extension functions."""
        patterns = [
            r'fun\s+\w+\.\w+\(',  # Kotlin extension function definitions
            r'extension\s+\w+',    # Swift extension definitions
            r'isNotNullOrEmpty',   # Specific function we're looking for
            r'isNullOrEmpty',      # Related function
            r'isEmpty',            # Common Swift function
            r'guard\s+let',        # Swift guard statements
            r'if\s+let',           # Swift optional binding
        ]
        return self.find_issue_locations(diff, patterns)
    
    def extract_import_issues(self, diff: str) -> List[DiffLocation]:
        """Extract issues related to imports."""
        patterns = [
            r'^import\s+',  # Import statements
            r'^-\s*import\s+',  # Removed imports
            r'^\+\s*import\s+',  # Added imports
            r'import\s+Foundation',  # Foundation imports
            r'import\s+SwiftUI',     # SwiftUI imports
            r'import\s+UIKit',       # UIKit imports
        ]
        return self.find_issue_locations(diff, patterns)
    
    def extract_documentation_issues(self, diff: str) -> List[DiffLocation]:
        """Extract issues related to missing documentation."""
        patterns = [
            r'//\s*TODO',  # TODO comments
            r'//\s*FIXME',  # FIXME comments
            r'/\*\*',  # JavaDoc comments
            r'//\s*',  # Regular comments
            r'///',     # Swift documentation comments
            r'// MARK:', # Swift MARK comments
        ]
        return self.find_issue_locations(diff, patterns)
    
    def extract_swift_issues(self, diff: str) -> List[DiffLocation]:
        """Extract Swift-specific issues."""
        patterns = [
            r'!\s*$',           # Force unwrapping at end of line
            r'as!\s+\w+',       # Force casting
            r'print\s*\(',      # Print statements (should use proper logging)
            r'NSLog\s*\(',      # NSLog statements
            r'DispatchQueue\.main\.async',  # Main queue dispatching
            r'@IBOutlet',       # IBOutlets
            r'@IBAction',       # IBActions
            r'weak\s+var',      # Weak references
            r'unowned\s+var',   # Unowned references
        ]
        return self.find_issue_locations(diff, patterns)
