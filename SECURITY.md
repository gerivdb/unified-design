# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.1.x   | ✅        |
| < 2.1   | ❌        |

## Reporting a Vulnerability

Report security vulnerabilities to the maintainers via the contact
information in `CODEOWNERS`. Do not open public issues for security
vulnerabilities.

## Security Measures

- All dependencies are scanned for vulnerabilities
- Pre-commit hooks enforce ASCII-only source (no obfuscation)
- BDCP mode enforced (no external network exposure during development)
- Secrets scanning via pre-commit

## Scope

This policy covers the unified-design repository and its direct dependencies.