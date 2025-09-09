from typing import Dict, Any, List
from enum import Enum


class PlatformType(Enum):
    ANDROID = "android"
    IOS = "ios"
    BACKEND = "backend"
    UNKNOWN = "unknown"


class PlatformDetectionService:
    """Service to detect the platform type of a PR based on repository name and file changes."""
    
    def __init__(self):
        # Android indicators
        self.android_repo_patterns = [
            "android", "consumer-android", "provider-android"
        ]
        self.android_file_patterns = [
            ".kt", ".kts", ".java", "build.gradle", "AndroidManifest.xml",
            "activity", "fragment", "viewmodel", "compose", "jetpack"
        ]
        
        # iOS indicators
        self.ios_repo_patterns = [
            "ios", "consumer-ios", "provider-ios"
        ]
        self.ios_file_patterns = [
            ".swift", ".m", ".h", "Info.plist", "Podfile", "Package.swift",
            "swiftui", "uikit", "viewmodel", "viewcontroller"
        ]
        
        # Backend indicators
        self.backend_repo_patterns = [
            "service", "api", "backend", "server", "gateway", "auth", "billing",
            "payment", "communication", "appointment", "consultation", "scheduler"
        ]
        self.backend_file_patterns = [
            ".py", ".js", ".ts", ".java", ".go", ".php", ".rb", ".cs",
            "controller", "service", "repository", "model", "api", "endpoint",
            "dockerfile", "requirements.txt", "package.json", "pom.xml"
        ]
    
    def detect_platform(self, repository: str, file_changes: List[str] = None) -> PlatformType:
        """
        Detect the platform type based on repository name and file changes.
        
        Args:
            repository: Repository name
            file_changes: List of changed file paths (optional)
            
        Returns:
            PlatformType enum
        """
        # First, check repository name patterns
        repo_lower = repository.lower()
        
        # Check Android patterns
        if any(pattern in repo_lower for pattern in self.android_repo_patterns):
            return PlatformType.ANDROID
        
        # Check iOS patterns
        if any(pattern in repo_lower for pattern in self.ios_repo_patterns):
            return PlatformType.IOS
        
        # Check Backend patterns
        if any(pattern in repo_lower for pattern in self.backend_repo_patterns):
            return PlatformType.BACKEND
        
        # If file changes are provided, analyze them
        if file_changes:
            return self._detect_from_files(file_changes)
        
        return PlatformType.UNKNOWN
    
    def _detect_from_files(self, file_changes: List[str]) -> PlatformType:
        """Detect platform from file changes."""
        android_score = 0
        ios_score = 0
        backend_score = 0
        
        for file_path in file_changes:
            file_lower = file_path.lower()
            
            # Score Android files
            if any(pattern in file_lower for pattern in self.android_file_patterns):
                android_score += 1
            
            # Score iOS files
            if any(pattern in file_lower for pattern in self.ios_file_patterns):
                ios_score += 1
            
            # Score Backend files
            if any(pattern in file_lower for pattern in self.backend_file_patterns):
                backend_score += 1
        
        # Return the platform with highest score
        if android_score > ios_score and android_score > backend_score:
            return PlatformType.ANDROID
        elif ios_score > android_score and ios_score > backend_score:
            return PlatformType.IOS
        elif backend_score > android_score and backend_score > ios_score:
            return PlatformType.BACKEND
        
        return PlatformType.UNKNOWN
    
    def get_platform_checklist(self, platform: PlatformType) -> Dict[str, Any]:
        """Get the platform-specific checklist for review."""
        
        if platform == PlatformType.ANDROID:
            return {
                "platform": "Android/Kotlin",
                "checklist": {
                    "architecture": [
                        "✅ Architecture respected (MVVM / Clean / Repository pattern)",
                        "✅ Proper use of ViewModel, LiveData / StateFlow",
                        "✅ No business logic inside Activities/Fragments"
                    ],
                    "null_safety": [
                        "✅ Null safety enforced (?., ?:, let, requireNotNull)",
                        "✅ Avoid use of !! (force unwrap)"
                    ],
                    "ui_components": [
                        "✅ Reusable UI components (Compose / XML) extracted properly",
                        "✅ Jetpack Compose previews or UI tests available",
                        "✅ Strings, colors, and dimensions use resources (no hardcoding)",
                        "✅ App supports both light/dark theme modes"
                    ],
                    "lifecycle": [
                        "✅ Proper lifecycle handling (coroutines / flows canceled on destroy)"
                    ],
                    "networking": [
                        "✅ Network/API calls handled in Repository layer, not UI layer",
                        "✅ API error handling included (timeouts, 4xx/5xx handling)"
                    ],
                    "dependency_injection": [
                        "✅ Dependency Injection followed (Hilt / Koin / Dagger)"
                    ],
                    "database": [
                        "✅ Room/Database queries optimized (no main-thread DB calls)"
                    ],
                    "accessibility": [
                        "✅ Accessibility labels and content descriptions added for UI elements"
                    ],
                    "permissions": [
                        "✅ App permissions requested and justified properly"
                    ],
                    "performance": [
                        "✅ Large bitmaps/images handled efficiently (avoid OOM)"
                    ],
                    "logging": [
                        "✅ Logging cleaned up (no debug/secret logs)"
                    ],
                    "dependencies": [
                        "✅ Gradle dependencies updated, no unused libraries"
                    ]
                }
            }
        
        elif platform == PlatformType.IOS:
            return {
                "platform": "iOS/Swift",
                "checklist": {
                    "architecture": [
                        "✅ Architecture respected (MVVM / Clean / Repository pattern)",
                        "✅ Proper use of @State, @ObservedObject, @EnvironmentObject, @StateObject",
                        "✅ No business logic inside Views — kept in ViewModel / UseCase"
                    ],
                    "optionals": [
                        "✅ No force unwrapping (!) unless safely guarded",
                        "✅ Optionals handled properly (if let, guard let)"
                    ],
                    "ui_components": [
                        "✅ Reusable UI components (SwiftUI Views / UIKit Components) extracted",
                        "✅ Accessibility labels and traits added for UI elements",
                        "✅ Strings, fonts, and colors use design system (no hardcoding)",
                        "✅ .scaledFont and dynamic type supported for accessibility"
                    ],
                    "navigation": [
                        "✅ Navigation flows handled consistently (NavigationStack / Router)"
                    ],
                    "error_handling": [
                        "✅ Proper error handling (e.g., network failures, decoding errors)"
                    ],
                    "networking": [
                        "✅ Network/API calls handled in Repository layer, not directly in ViewModels"
                    ],
                    "dependency_injection": [
                        "✅ Dependency Injection used (Factory / Resolver / Swift Dependency Injection)"
                    ],
                    "performance": [
                        "✅ Animations smooth and don't block main thread",
                        "✅ Background tasks handled properly (URLSession, Task, Combine)",
                        "✅ Memory usage reviewed (no retain cycles, weak/unowned used where needed)"
                    ],
                    "logging": [
                        "✅ No debug/print logs in production code"
                    ],
                    "testing": [
                        "✅ Unit/UI tests cover main logic and edge cases"
                    ],
                    "dependencies": [
                        "✅ Frameworks/SDKs up to date, no unused dependencies"
                    ]
                }
            }
        
        elif platform == PlatformType.BACKEND:
            return {
                "platform": "Backend",
                "checklist": {
                    "architecture": [
                        "✅ Architecture & Design",
                        "  • Layers respected (Controller → Service → Repository → DB)",
                        "  • Business logic not mixed inside controllers",
                        "  • Code modular and reusable"
                    ],
                    "api_contracts": [
                        "✅ API Contracts",
                        "  • Request/response schemas validated",
                        "  • Consistent status codes (2xx, 4xx, 5xx)",
                        "  • Proper error messages returned (no raw stack traces)",
                        "  • Versioning followed (no breaking changes)"
                    ],
                    "data_handling": [
                        "✅ Data Handling",
                        "  • Null/empty input validated",
                        "  • SQL/NoSQL queries optimized (indexes used where needed)",
                        "  • No N+1 query issues",
                        "  • Pagination added for large responses"
                    ],
                    "security": [
                        "✅ Security",
                        "  • No hardcoded secrets (keys, passwords, tokens)",
                        "  • Environment variables used for configs",
                        "  • Authentication & authorization enforced (JWT, OAuth, etc.)",
                        "  • Input/output sanitized to prevent SQLi, XSS, injections",
                        "  • Sensitive data encrypted at rest and in transit (HTTPS, TLS)"
                    ],
                    "performance": [
                        "✅ Performance & Reliability",
                        "  • Caching applied where beneficial",
                        "  • Async/background jobs used for heavy tasks",
                        "  • Retry and timeout logic for external calls",
                        "  • Rate limiting/throttling where needed",
                        "  • Logs optimized (no sensitive data, no log flooding)"
                    ],
                    "error_handling": [
                        "✅ Error Handling & Monitoring",
                        "  • Try/catch or error middleware present",
                        "  • Custom error codes/messages consistent",
                        "  • Monitoring/alerts integrated (Prometheus, Datadog, etc.)"
                    ],
                    "testing": [
                        "✅ Testing",
                        "  • Unit tests cover core logic",
                        "  • Integration tests for APIs/DB",
                        "  • Mocks/stubs used where external dependencies exist",
                        "  • Test data anonymized (no production secrets)"
                    ],
                    "documentation": [
                        "✅ Documentation & Deployment",
                        "  • API docs updated (Swagger / Postman collection)",
                        "  • Config/migration steps documented",
                        "  • CI/CD pipeline checks passing",
                        "  • Docker/Kubernetes manifests updated if needed"
                    ]
                }
            }
        
        else:
            return {
                "platform": "Unknown",
                "checklist": {
                    "general": [
                        "✅ Code follows established patterns and conventions",
                        "✅ No hardcoded values or secrets",
                        "✅ Proper error handling implemented",
                        "✅ Tests cover main functionality",
                        "✅ Documentation updated if needed"
                    ]
                }
            }
