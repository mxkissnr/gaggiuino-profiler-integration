# Security Policy

## Supported Versions

Only the **latest release** receives security fixes. Please update before reporting.

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Send a private report to **maximilian.kissner24@gmail.com** with:

- A clear description of the vulnerability
- Steps to reproduce (proof-of-concept if possible)
- Potential impact

I will acknowledge your report within **7 days** and aim to release a fix within **30 days** depending on severity.

## Scope

This integration runs locally inside Home Assistant and communicates only with the GLP add-on on the same instance. The primary attack surface is:

- HTTP requests to the GLP add-on API (token-authenticated)
- Entity attribute data (JSON from the add-on)
- The HA config entry (stores the add-on URL)

Out of scope: vulnerabilities in Home Assistant itself or the GLP add-on (report those in their respective repositories).
