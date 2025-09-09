# Security Policy

## Supported Versions

We currently support the following versions of the Bitbucket PR Reviewer MCP Server:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

### How to Report

1. **DO NOT** create a public GitHub issue
2. **DO NOT** disclose the vulnerability publicly until it has been addressed
3. Send an email to: [security@example.com](mailto:security@example.com)
4. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- We will acknowledge receipt within 48 hours
- We will provide regular updates on our progress
- We will credit you in our security advisories (unless you prefer to remain anonymous)
- We will work with you to ensure the vulnerability is properly addressed

## Security Features

This project includes several security features:

### 🔒 Credential Protection
- Automatic sanitization of sensitive data before sending to AI models
- Comprehensive pattern matching for 20+ credential types
- No sensitive information reaches external AI services

### 🛡️ Input Validation
- All inputs are validated using Pydantic models
- Environment variables are properly sanitized
- API responses are validated before processing

### 🔐 Secure Configuration
- All sensitive configuration via environment variables
- No hardcoded secrets or credentials
- Proper error handling without information disclosure

### 🚫 Access Control
- Bitbucket API access limited to required permissions only
- No unnecessary data exposure
- Proper authentication handling

## Security Best Practices

### For Users
1. **Use App Passwords**: Never use your main Bitbucket password
2. **Limit Permissions**: Only grant necessary permissions to the App Password
3. **Regular Rotation**: Rotate your App Password regularly
4. **Environment Variables**: Store credentials in environment variables, not in code
5. **Review Comments**: Always review AI-generated comments before posting

### For Developers
1. **No Hardcoded Secrets**: Never commit secrets to version control
2. **Input Validation**: Always validate and sanitize inputs
3. **Error Handling**: Don't expose sensitive information in error messages
4. **Dependencies**: Keep dependencies updated and scan for vulnerabilities
5. **Code Review**: Always review code for security issues

## Known Security Considerations

### Credential Sanitization
The project automatically sanitizes sensitive information from PR diffs before sending them to AI models. However, users should:

- Review the sanitization patterns in `src/config/settings.py`
- Add custom patterns for their specific credential types
- Test sanitization with their own data before using in production

### API Access
The project requires Bitbucket API access with the following permissions:
- **Repositories: Read** - To fetch PR data and diffs
- **Pull requests: Read and Write** - To post comments

### Data Handling
- PR diffs are processed locally before sanitization
- Sanitized data is sent to AI models for analysis
- No raw PR data is stored or logged
- Comments are posted directly to Bitbucket

## Security Updates

Security updates will be released as needed. We recommend:

1. **Regular Updates**: Keep the project updated to the latest version
2. **Dependency Updates**: Regularly update dependencies
3. **Security Monitoring**: Monitor for security advisories
4. **Vulnerability Scanning**: Use tools to scan for known vulnerabilities

## Contact

For security-related questions or concerns:
- Email: [security@example.com](mailto:security@example.com)
- GitHub: [Create a private security advisory](https://github.com/MdMugish/bitbucket-pr-reviewer-mcp/security/advisories/new)

---

**Last Updated**: December 2024
