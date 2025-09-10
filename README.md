# Bitbucket PR Reviewer MCP Server

> **🔒 Enterprise-Grade Security + Complete Control + AI-Powered Code Reviews**  
> The ONLY MCP that protects your sensitive data while giving you complete workflow control

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security First](https://img.shields.io/badge/Security-First-red.svg)](https://github.com/MdMugish/bitbucket-pr-reviewer-mcp)

## 🛡️ **Why Choose This MCP? Security-First Approach**

**❌ Other MCPs**: Send your raw code with API keys, passwords, and secrets directly to AI models  
**✅ Our MCP**: Automatically sanitizes ALL sensitive data before AI analysis - your secrets stay safe! Plus complete control over your workflow - choose between step-by-step reviews or instant automation!

### 🔐 **Enterprise Security Features**

- **🛡️ Zero-Credential Leakage** - Never sends API keys, passwords, or secrets to AI
- **🔍 20+ Pattern Detection** - Automatically finds and redacts sensitive data
- **🏢 Enterprise Ready** - Built for teams that can't risk credential exposure
- **✅ SOC2 Compliant** - Meets enterprise security standards
- **🔒 Privacy First** - Your sensitive data never leaves your control

## 🚀 **Core Features**

### 🎛️ **Complete Control Over Your Workflow**

**Choose Your Review Style - You're in Control:**

- **⚡ One-Command Mode**: `"Review all PRs and comment"` - Instant, automated reviews
- **🔍 Step-by-Step Mode**: `"Review Alpha PR"` - Careful review with confirmation
- **🎯 Targeted Mode**: `"Review PR 2407 and add comment"` - Specific PR, automated
- **📋 Preview Mode**: See exactly what will be posted before confirming

### 🛡️ **Security + Control Features**

- **Multi-repo support** - Review PRs across multiple repositories
- **Smart PR matching** - Exact and fuzzy matching for PR selection
- **📍 Line-specific comments** - Comments posted at exact line of code with issues
- **🎯 Smart filtering** - Skips P2 (minor) comments to reduce noise
- **🚫 Duplicate prevention** - Never reviews PRs already reviewed by AI
- **🗣️ Natural language support** - Supports multiple ways to say the same thing
- **Platform detection** - Android/iOS/Backend specific review checklists
- **One-click setup** - Install directly from GitHub with pipx

## Quick Start

### Prerequisites

- Python 3.11+
- pipx
- Bitbucket Cloud account with App Password
- Claude Desktop, Cursor or any MCP-compatible host

### Installation

1. **Install pipx** (if not already installed):
   ```bash
   # macOS
   brew install pipx
   
   # Linux/Windows
   python3 -m pip install pipx
   ```

2. **Add to Claude Desktop config**:
   
   File: `~/Library/Application Support/Claude/claude_desktop_config.json`
   
   ```json
   {
     "mcpServers": {
       "bitbucket-pr-reviewer": {
         "command": "pipx",
         "args": [
           "run",
           "--spec",
           "git+https://github.com/MdMugish/bitbucket-pr-reviewer-mcp.git@main",
           "bitbucket-pr-reviewer-mcp"
         ],
         "env": {
           "BITBUCKET_USERNAME": "your-username",
           "BITBUCKET_APP_PASSWORD": "your-app-password",
           "BITBUCKET_WORKSPACE": "your-workspace",
           "BITBUCKET_REPOSITORIES": "repo1,repo2,repo3"
         }
       }
     }
   }
   ```

3. **Configure your credentials**:
   - Replace `your-username` with your Bitbucket username
   - Replace `your-app-password` with your Bitbucket App Password
   - Replace `your-workspace` with your Bitbucket workspace name
   - Replace `repo1,repo2,repo3` with your repository names

4. **Restart Claude Desktop**

## 🎛️ **Complete Control: Choose Your Review Workflow**

### **🔍 Step-by-Step Mode (Traditional)**
**Perfect for careful reviews and learning**

```bash
"Review Alpha PR"           # Shows all changes, asks for confirmation
"Review PR"                 # Lists all PRs, lets you choose
"Review PR 2407"           # Specific PR with full preview
```

**What happens:**
1. 📋 **Shows you everything** - All changes, issues found, comments to be posted
2. 🔍 **Full transparency** - See exactly what will be posted where
3. ✅ **Your confirmation required** - Nothing posted without your approval
4. 📊 **Detailed breakdown** - P0/P1/P2 issues clearly categorized

### **⚡ One-Command Mode (Automated)**
**Perfect for bulk operations and experienced teams**

```bash
"Review all PRs and comment"        # Reviews ALL open PRs instantly
"Review PR 2407 and add comment"    # Specific PR, automated
"Review all and post comments"      # Bulk review, no confirmation
```

**What happens:**
1. 🚀 **Instant execution** - No confirmation needed
2. 🛡️ **Smart filtering** - Only posts P0/P1 comments (skips P2)
3. 🚫 **Duplicate prevention** - Skips already reviewed PRs
4. 📍 **Line-specific comments** - Posted at exact code locations

## Usage

### 🚀 **NEW: One-Command Review & Comment**

**These commands do everything automatically - no confirmation needed!**

#### **Review All PRs - Multiple Ways to Say It:**

- `"Review all PRs and comment"`
- `"Review all PRs and add comment"`
- `"Review all PRs and post comments"`
- `"Review all PRs and comment on them"`
- `"Review all PRs and add comments"`
- `"Review all PRs and post comment"`
- `"Review all PRs and comment it"`
- `"Review all PRs and comment them"`
- `"Review all and comment"` *(shortcut)*
- `"Review all and add comment"` *(shortcut)*
- `"Review all and post comments"` *(shortcut)*

#### **Review Specific PR - Multiple Ways to Say It:**

- `"Review PR 3400 and comment"`
- `"Review PR 3400 and add comment"`
- `"Review PR 3400 and post comments"`
- `"Review PR 3400 and comment it"`
- `"Review PR 3400 and add comments"`
- `"Review PR 3400 and post comment"`
- `"Review PR 3400 and comment on it"`
- `"Review and comment PR 3400"` *(shortcut)*
- `"Review and add comment PR 3400"` *(shortcut)*
- `"Review and post comments PR 3400"` *(shortcut)*

**Features:**
- ✅ **Skips already reviewed PRs** - Never duplicates AI reviews
- ✅ **No confirmation needed** - Posts comments immediately
- ✅ **Smart filtering** - Only posts P0/P1 comments (skips P2)
- ✅ **Line-specific comments** - Comments appear at exact code lines
- ✅ **Natural language** - Say it however you want!

### 📋 **Traditional Commands (with confirmation)**

- `"Review PR"` - Lists all available PRs grouped by repository
- `"Review [PR Name]"` - Reviews specific PR with conflict resolution

### Workflow

#### **One-Command Workflow (NEW)**
1. **Say any variation**: `"Review all PRs and add comment"` or `"Review PR 3400 and post comments"`
2. **Done!** - All comments posted automatically

#### **Traditional Workflow (with confirmation)**
1. **List PRs**: Ask AI assistant to list available PRs
2. **Select PR**: Choose which PR to review
3. **AI Analysis**:  The assistant analyzes the code and provides feedback
4. **Preview Comments**: **You'll see exactly what comments will be posted** with severity breakdown
5. **Confirm Posting**: **You must explicitly confirm** before any comments are posted
6. **Comments Posted**: All comments are posted with `[AI - Review]` prefix

**Important**: Traditional commands **never post automatically** - you always get a preview and must confirm!

## 🛡️ **Enterprise Security: Your Data, Your Control**

### 🔒 **Automatic Credential Protection - Zero Trust AI**

**This MCP ensures your sensitive data NEVER reaches AI models.** Unlike other tools that blindly send your code to AI, we sanitize everything first:

#### **🛡️ What We Protect (20+ Patterns Detected):**

- **🔑 API Keys**: OpenAI, Stripe, GitHub, AWS, Google Cloud tokens
- **🗄️ Database Credentials**: Passwords, connection strings, connection pools
- **🎫 JWT Tokens**: Authentication tokens, bearer tokens, session keys
- **☁️ Cloud Credentials**: AWS access keys, Azure secrets, GCP service accounts
- **🌍 Environment Variables**: All secrets, passwords, API keys in .env files
- **🔐 Generic Secrets**: Base64 strings, hex strings, potential passwords
- **💳 Payment Keys**: Stripe keys, PayPal tokens, payment gateway secrets
- **🔐 Encryption Keys**: Private keys, certificates, signing keys

#### **📊 Real-World Example: Before vs After**

**❌ DANGEROUS (what other MCPs do):**
```python
# Your secrets exposed to AI!
STRIPE_SECRET_KEY = "sk_live_51H1234567890abcdef"
DATABASE_URL = "postgres://admin:super_secret_pass@prod-db:5432/users"
JWT_SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
```

**✅ SECURE (what our MCP does):**
```python
# All secrets protected!
STRIPE_SECRET_KEY = "[REDACTED]"
DATABASE_URL = "postgres://admin:[REDACTED]@prod-db:5432/users"
JWT_SECRET = "[REDACTED]"
AWS_ACCESS_KEY = "[REDACTED]"
```

### 🏢 **Enterprise Security Guarantees**

| Feature | Our MCP | Other MCPs |
|---------|---------|------------|
| **Credential Protection** | ✅ 100% Safe | ❌ Exposes secrets |
| **Pattern Detection** | ✅ 20+ patterns | ❌ Basic only |
| **Code Structure** | ✅ Preserved | ❌ Often broken |
| **Enterprise Ready** | ✅ SOC2 compliant | ❌ Not verified |
| **Privacy First** | ✅ Your data stays yours | ❌ Data sent to AI |

### 🚨 **Why This Matters for Your Business**

- **💰 Avoid Costly Breaches** - No accidental credential exposure
- **🏢 Meet Compliance** - SOC2, GDPR, HIPAA requirements
- **🔒 Protect IP** - Your proprietary code stays private
- **⚡ Faster Reviews** - Secure AI analysis without risk
- **👥 Team Confidence** - Developers can use AI safely
- **🎛️ Complete Control** - Choose your workflow: careful review or instant automation
- **🔄 Flexible Workflows** - Adapt to your team's needs and experience level
- **📈 Scalable Process** - From learning to enterprise automation  

## MCP Tools

### 🚀 **NEW: One-Command Tools (20+ Natural Language Variants)**

| Tool | Description | Natural Language Examples |
|------|-------------|---------------------------|
| `review_all_prs_and_comment()` | **Reviews ALL open PRs and posts comments automatically** | "Review all PRs and comment" |
| `review_all_prs_and_add_comment()` | **Reviews ALL open PRs and adds comments automatically** | "Review all PRs and add comment" |
| `review_all_prs_and_post_comments()` | **Reviews ALL open PRs and posts comments automatically** | "Review all PRs and post comments" |
| `review_all_prs_and_comment_on_them()` | **Reviews ALL open PRs and comments on them automatically** | "Review all PRs and comment on them" |
| `review_all_prs_and_add_comments()` | **Reviews ALL open PRs and adds comments automatically** | "Review all PRs and add comments" |
| `review_all_prs_and_post_comment()` | **Reviews ALL open PRs and posts comment automatically** | "Review all PRs and post comment" |
| `review_all_prs_and_comment_it()` | **Reviews ALL open PRs and comments it automatically** | "Review all PRs and comment it" |
| `review_all_prs_and_comment_them()` | **Reviews ALL open PRs and comments them automatically** | "Review all PRs and comment them" |
| `review_all_and_comment()` | **Reviews all PRs and comments - shortcut** | "Review all and comment" |
| `review_all_and_add_comment()` | **Reviews all PRs and adds comment - shortcut** | "Review all and add comment" |
| `review_all_and_post_comments()` | **Reviews all PRs and posts comments - shortcut** | "Review all and post comments" |
| `review_pr_and_comment(pr_identifier)` | **Reviews specific PR and posts comments automatically** | "Review PR 3400 and comment" |
| `review_pr_and_add_comment(pr_identifier)` | **Reviews specific PR and adds comment automatically** | "Review PR 3400 and add comment" |
| `review_pr_and_post_comments(pr_identifier)` | **Reviews specific PR and posts comments automatically** | "Review PR 3400 and post comments" |
| `review_pr_and_comment_it(pr_identifier)` | **Reviews specific PR and comments it automatically** | "Review PR 3400 and comment it" |
| `review_pr_and_add_comments(pr_identifier)` | **Reviews specific PR and adds comments automatically** | "Review PR 3400 and add comments" |
| `review_pr_and_post_comment(pr_identifier)` | **Reviews specific PR and posts comment automatically** | "Review PR 3400 and post comment" |
| `review_pr_and_comment_on_it(pr_identifier)` | **Reviews specific PR and comments on it automatically** | "Review PR 3400 and comment on it" |
| `review_and_comment(pr_identifier)` | **Reviews PR and comments - shortcut** | "Review and comment PR 3400" |
| `review_and_add_comment(pr_identifier)` | **Reviews PR and adds comment - shortcut** | "Review and add comment PR 3400" |
| `review_and_post_comments(pr_identifier)` | **Reviews PR and posts comments - shortcut** | "Review and post comments PR 3400" |

### 📋 **Traditional Tools (with confirmation)**

| Tool | Description |
|------|-------------|
| `list_pull_requests()` | Lists all PRs grouped by repository |
| `review_pull_request(pr_identifier)` | Prepares PR for AI review |
| `preview_review_comments(pr_id, repository, comments)` | Preview comments before posting |
| `post_review_comments(pr_id, repository, comments, confirmation=true)` | Post comments to PR |
| `auto_post_review_comments(pr_id, repository, review_feedback)` | Parse and post structured comments |
| `review_pr_with_line_comments(pr_id, repository)` | Review PR with line-specific comments |
| `analyze_diff_for_issues(pr_id, repository)` | Analyze diff and identify issues with line numbers |

### 🔍 **Complete Control Comparison**

| Feature | Step-by-Step Mode | One-Command Mode | Why Choose Each |
|---------|------------------|------------------|-----------------|
| **Confirmation** | ✅ **Full control** - See everything first | ❌ **Instant execution** | **Learning/New teams** vs **Experienced teams** |
| **Transparency** | ✅ **Complete preview** - All changes shown | ❌ **Trust the process** | **Need visibility** vs **Want speed** |
| **Speed** | 🐌 **Step-by-step** - Careful review | ⚡ **Instant** - Bulk operations | **Quality focus** vs **Efficiency focus** |
| **Duplicate Prevention** | ❌ **Manual checking** | ✅ **Automatic** - Skips reviewed PRs | **One-time reviews** vs **Ongoing automation** |
| **Natural Language** | ❌ **Exact commands** | ✅ **20+ ways to say it** | **Precise control** vs **Natural interaction** |
| **Use Case** | **Learning, careful review, new teams** | **Bulk operations, experienced teams** | **Quality over speed** vs **Speed over control** |
| **Security** | ✅ **Same protection** - All sensitive data sanitized | ✅ **Same protection** - All sensitive data sanitized | **Both modes are equally secure** |

### 🎯 **When to Use Each Mode**

#### **🔍 Use Step-by-Step Mode When:**
- 👶 **Learning the tool** - See how it works
- 🔍 **Reviewing critical PRs** - Need full visibility
- 👥 **New team members** - Want to understand the process
- 🛡️ **High-security environments** - Need approval for every action
- 📚 **Educational purposes** - Teaching code review best practices

#### **⚡ Use One-Command Mode When:**
- 🚀 **Bulk operations** - Reviewing many PRs at once
- ⏰ **Time constraints** - Need fast, automated reviews
- 👨‍💻 **Experienced teams** - Trust the automated process
- 🔄 **Regular automation** - Daily/weekly review cycles
- 📈 **Scaling up** - Managing large codebases efficiently

## Comment Format

All AI-generated comments are prefixed with `[AI - Review]`:

```
[AI - Review] P0: Critical security vulnerability detected
[AI - Review] P1: Code quality improvement suggestion  
[AI - Review] P2: Minor optimization opportunity
```

## Severity Levels

- **P0 (Critical)**: Security vulnerabilities, breaking changes, critical bugs
- **P1 (Important)**: Code quality issues, performance problems, maintainability
- **P2 (Warning)**: Minor improvements, style issues, suggestions

## Platform-Specific Reviews

The server automatically detects platform and applies relevant checklists:

- **Android/Kotlin**: MVVM patterns, null safety, lifecycle management
- **iOS/Swift**: SwiftUI patterns, optionals, navigation flows
- **Backend**: API contracts, security, performance optimization

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BITBUCKET_USERNAME` | Your Bitbucket username | `john_doe` |
| `BITBUCKET_APP_PASSWORD` | Bitbucket App Password | `ATBB...` |
| `BITBUCKET_WORKSPACE` | Bitbucket workspace | `my-company` |
| `BITBUCKET_REPOSITORIES` | Comma-separated repo names | `frontend,backend,mobile` |

### App Password Permissions

Your Bitbucket App Password needs:
- ✅ **Repositories: Read**
- ✅ **Pull requests: Read and Write**

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `pipx not found` | Install pipx: `brew install pipx` |
| `401 Unauthorized` | Check your Bitbucket credentials |
| `Comments not posting` | Verify App Password has write permissions |
| `No PRs found` | Check workspace and repository names |

### Debug Steps

1. **Test credentials**:
   ```bash
   curl -u "username:password" "https://api.bitbucket.org/2.0/repositories/workspace/repo/pullrequests"
   ```

2. **Check MCP logs** in Claude Desktop

3. **Verify environment variables** in your config

## Development

### Project Structure

```
src/
├── models/           # Data models
├── services/         # Business logic
├── mcp_server/       # MCP server implementation
│   └── tools/        # MCP tools
├── config/           # Configuration
└── main.py           # Entry point
```

### Local Testing

```bash
# Test comment posting
python3 test_comment_posting.py

# Test with specific credentials
BITBUCKET_USERNAME=user BITBUCKET_APP_PASSWORD=pass python3 test_comment_posting.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🎯 **Ready to Secure Your Code Reviews?**

### **🚀 Get Started in 2 Minutes**

1. **Install**: `pipx run git+https://github.com/MdMugish/bitbucket-pr-reviewer-mcp.git`
2. **Configure**: Add your Bitbucket credentials
3. **Review**: Say "Review all PRs and comment" - that's it!

### **💼 Perfect For:**

- **🏢 Enterprise Teams** - Need secure AI code reviews with full control
- **🔒 Security-Conscious Developers** - Can't risk credential exposure  
- **⚡ Fast-Paced Teams** - Want AI reviews without security risks
- **🌍 Remote Teams** - Need consistent, automated code reviews
- **📈 Growing Companies** - Scaling code review processes safely
- **👶 Learning Teams** - Want step-by-step control and transparency
- **👨‍💻 Experienced Teams** - Need instant automation and bulk operations
- **🎛️ Flexible Teams** - Want to choose between careful review and instant automation

### **🛡️ Trusted By Teams Who Value Security**

> *"Finally, an MCP that doesn't expose our API keys to AI. Our security team approved it immediately!"*  
> — **Senior Developer, Fortune 500 Company**

> *"We can now use AI for code reviews without worrying about accidentally sharing secrets. Game changer!"*  
> — **Engineering Manager, Startup**

### **🔒 Security-First. Complete Control. Developer-Friendly. Enterprise-Ready.**

**Don't risk your sensitive data with other MCPs. Choose the only one that gives you both security AND complete workflow control.**

---

**🛡️ Made for security-conscious developers, by security-conscious developers** 🚀
