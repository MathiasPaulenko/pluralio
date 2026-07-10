# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |
| < 0.1 | No |

## Reporting a vulnerability

If you discover a security vulnerability in pluralio, please report it responsibly.

**Do not open a public GitHub issue.**

Instead, email **<mathias.paulenko@outlook.com>** with:

1. A description of the vulnerability
2. Steps to reproduce or a proof of concept
3. The potential impact
4. Any suggested fixes (optional)

You will receive a response within 48 hours. If the vulnerability is confirmed, a fix will be prioritized and a security advisory will be published on GitHub.

## Disclosure policy

- We acknowledge receipt of your report within 48 hours
- We investigate and confirm the vulnerability within 7 days
- We release a fix and publish a security advisory
- We credit the reporter (unless they prefer to remain anonymous)

## Security considerations

pluralio is a pure-Python library with zero runtime dependencies. It does not:

- Execute arbitrary code
- Make network requests
- Read or write files
- Interact with the operating system

The attack surface is minimal. The most likely security concern would be a ReDoS (Regular Expression Denial of Service) vulnerability in the regex rules. If you find such a pattern, please report it following the process above.
