---
name: aegisx-cybersecurity-development
description: Development guidelines and implementation instructions for AegisX, an AI-powered cybersecurity assessment platform.
---

# AegisX Development Skill

## Project Identity

AegisX is an AI-Powered Cybersecurity Assessment Platform designed for authorized security assessment of websites, domains, and servers.

This project must be developed as a professional, modular, portfolio-worthy cybersecurity platform.

## Core Engineering Rules

- Inspect the existing repository before making changes.
- Preserve existing working code.
- Follow the PRD, SRS, System Design, and Development Log as the source of truth.
- Do not blindly rewrite the project.
- Build modules that integrate into the complete application.
- Use clean architecture and modular Python code.
- Handle errors gracefully.
- Add meaningful tests.
- Never hardcode API keys, passwords, or secrets.

## Defensive Security Boundary

Only implement defensive and authorized cybersecurity assessment features.

Do not implement exploitation, brute-force attacks, credential attacks, malware, destructive actions, payload delivery, persistence mechanisms, or unauthorized access techniques.

Display and preserve this principle:

"Only scan systems, domains, and infrastructure you own or are explicitly authorized to assess."

## Architecture

Follow this general flow:

User Input
→ Input Validation
→ Scan Orchestrator
→ Security Modules
→ Result Aggregation
→ Risk Engine
→ Recommendation Engine
→ Database
→ Dashboard
→ Reports
→ Optional AI Explanation

## Main Modules

Implement and maintain:

- Network Port Scanner
- Service Detection and Banner Grabbing
- HTTP Security Header Analysis
- SSL/TLS Certificate Inspection
- DNS Analysis
- WHOIS Lookup
- Risk Scoring Engine
- Security Recommendation Engine
- SQLite Scan History
- Streamlit Dashboard
- PDF Report Generation
- CSV Export
- Optional AI Security Explanation Layer

## Coding Rules

- Follow PEP 8.
- Use clear names and type hints where practical.
- Keep functions focused.
- Keep UI separate from business logic.
- Avoid a giant monolithic app.py.
- Use structured results.
- Use configurable timeouts for network operations.
- A failure in one scan module must not crash the entire assessment.
- Never execute shell commands using user-controlled input.
- Never use shell=True for scanning operations.

## Working Process

Before implementing a major change:

1. Inspect relevant files.
2. Check the project documentation.
3. Identify files to modify.
4. Implement the change.
5. Run relevant tests or checks.
6. Report what works and any limitations.

Work through these milestones:

1. Repository Audit
2. Core Foundation
3. Security Modules
4. Risk and Recommendations
5. Database and Scan History
6. Authentication
7. Professional UI/UX
8. PDF and CSV Reporting
9. AI Integration
10. Testing and Hardening
11. GitHub Release Preparation

## Final Goal

The application should run using:

streamlit run app.py

The final system should provide a professional, integrated, authorized cybersecurity assessment workflow with real scan results, transparent risk scoring, actionable recommendations, scan history, reporting, and optional AI-powered explanations.