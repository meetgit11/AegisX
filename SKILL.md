---
name: aegisx-cybersecurity-development
description: Development skill and engineering guidelines for AegisX – AI-Powered Cybersecurity Assessment Platform. Use this skill when implementing, modifying, debugging, testing, reviewing, or documenting the AegisX project.
version: 1.0.0
---

# AegisX Development Skill

## Project Identity

**Project Name:** AegisX – AI-Powered Cybersecurity Assessment Platform

AegisX is a professional, modular cybersecurity assessment platform designed to assess the external security posture of websites, domains, and servers.

This is not a basic tutorial project or a simple port scanner.

The project is intended to demonstrate:

- Software engineering
- Cybersecurity fundamentals
- Computer networking
- Security analysis
- Modular architecture
- Database design
- Dashboard development
- Report generation
- Testing and debugging
- AI integration

The final project should be professional, functional, portfolio-worthy, and suitable for:

- Resume and portfolio
- Placement interviews
- Hackathon demonstrations
- GitHub showcase
- Cybersecurity learning

---

# Core Development Philosophy

Follow these principles:

1. Learn by Building.
2. Build production-style features, not fake demonstrations.
3. Preserve existing working code.
4. Do not rewrite the entire project unless explicitly necessary.
5. Prefer clean, modular, maintainable code.
6. Integrate features end-to-end.
7. Handle failures gracefully.
8. Keep cybersecurity features defensive and authorized.
9. Do not implement unnecessary complexity.
10. Do not leave non-functional placeholder features.

Before making significant changes:

1. Inspect the existing repository.
2. Read relevant documentation.
3. Understand existing implementations.
4. Identify dependencies and integration points.
5. Explain major architectural changes before making them.

---

# Source of Truth

The following project documents define the intended requirements and architecture:

- PRD
- SRS
- System Design Document
- Development Log
- Existing GitHub repository

When documents conflict with existing code:

1. Preserve working functionality where possible.
2. Prefer the approved project requirements.
3. Avoid blindly deleting code.
4. Clearly identify architectural conflicts.
5. Resolve inconsistencies systematically.

---

# Existing Project Architecture

The project follows a modular architecture similar to:

```text
AegisX/
│
├── app.py
├── SKILL.md
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── assets/
│
├── config/
│   ├── __init__.py
│   ├── constants.py
│   └── settings.py
│
├── core/
│   ├── __init__.py
│   ├── scanner.py
│   ├── risk_engine.py
│   └── recommendations.py
│
├── modules/
│   ├── __init__.py
│   ├── port_scanner.py
│   ├── service_detector.py
│   ├── header_analyzer.py
│   ├── ssl_inspector.py
│   ├── dns_lookup.py
│   └── whois_lookup.py
│
├── dashboard/
│   ├── __init__.py
│   ├── charts.py
│   ├── pages.py
│   └── ui_components.py
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── schema.sql
│
├── reports/
│   ├── __init__.py
│   ├── pdf_report.py
│   └── csv_export.py
│
├── tests/
│
├── docs/
│
└── outputs/
