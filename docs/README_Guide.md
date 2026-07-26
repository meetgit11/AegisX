\<div align="center"\>

\# 🛡️ AegisX – AI-Powered Cybersecurity Assessment Platform

\#\#\# \*Automated Reconnaissance, Attack Surface Mapping, and Heuristic Risk Scoring\*

\[\!\[Python Version\](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge\&logo=python\&logoColor=white)\](https://www.python.org/)  
\[\!\[UI Framework\](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg?style=for-the-badge\&logo=Streamlit\&logoColor=white)\](https://streamlit.io/)  
\[\!\[License: MIT\](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)\](LICENSE)  
\[\!\[Build Status\](https://img.shields.io/badge/Build-Passing-brightgreen.svg?style=for-the-badge)\]()  
\[\!\[PRs Welcome\](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge)\](CONTRIBUTING.md)

\---

\[Key Features\](\#-key-features) • \[Architecture\](\#%EF%B8%8F-architecture) • \[Quick Start\](\#-quick-start) • \[Tech Stack\](\#-tech-stack) • \[Roadmap\](\#%EF%B8%8F-future-roadmap)

\</div\>

\---

\#\# 📖 Introduction

\[cite\_start\]\*\*AegisX\*\* is an open-source, lightweight cybersecurity assessment platform designed to automate initial reconnaissance, external attack surface mapping, and vulnerability scoring for web applications and network endpoints\[cite: 11, 261\]. \[cite\_start\]By consolidating multi-threaded port scanning, banner grabbing, SSL/TLS inspection, HTTP security header auditing, and WHOIS/DNS intelligence into a single interactive \*\*Streamlit\*\* UI, AegisX lowers the barrier to entry for security auditing\[cite: 12, 190, 261\].

\[cite\_start\]Designed with defensive operations in mind, AegisX provides instant, actionable remediation steps, calculates a transparent risk score ($0.0 \- 10.0$), and compiles client-ready executive PDF and CSV reports in under 30 seconds\[cite: 13, 21, 23, 24, 28, 220\].

\---

\#\# ✨ Key Features

\* \[cite\_start\]🚀 \*\*Asynchronous Port Scanner:\*\* Rapidly probes top common TCP ports using non-blocking socket pools without requiring root privileges\[cite: 25, 37, 273, 291\].  
\* \[cite\_start\]🏷️ \*\*Banner Grabbing & Service Detection:\*\* Inspects server response signatures to determine underlying software versions\[cite: 26, 38, 212, 273\].  
\* \[cite\_start\]🔐 \*\*SSL/TLS Inspection:\*\* Evaluates certificate authority trust, validity periods, expiration alerts, and SSL protocol configurations\[cite: 26, 40, 215, 216\].  
\* \[cite\_start\]🌐 \*\*HTTP Security Header Audit:\*\* Checks for standard web security controls (\`HSTS\`, \`CSP\`, \`X-Frame-Options\`, \`X-Content-Type-Options\`)\[cite: 26, 39, 214\].  
\* \[cite\_start\]🔎 \*\*DNS & WHOIS Reconnaissance:\*\* Automatically queries A, AAAA, MX, TXT, and NS records alongside domain registrar data\[cite: 27, 41, 218, 219\].  
\* \[cite\_start\]📊 \*\*Heuristic Risk Engine:\*\* Uses rule-based weighting to compute a unified security posture rating ($0.0 \- 10.0$) with contextual remediations\[cite: 13, 23, 27, 42, 220\].  
\* \[cite\_start\]📄 \*\*Executive PDF & CSV Reports:\*\* One-click exports for printable PDF executive summaries and structured raw CSV audit files\[cite: 24, 28, 44, 222\].

\---

\#\# 📸 Screenshots & Demo Placeholder

\`\`\`text  
\+-----------------------------------------------------------------------------------+  
|                               AEGISX DASHBOARD UI                                 |  
\+-----------------------------------------------------------------------------------+  
| \[ Target Input: example.com \]                    \[ 🛡️ Start Assessment Button \] |  
|                                                                                   |  
|  \+---------------------+   \+---------------------+   \+-------------------------+  |  
|  | OVERALL RISK SCORE  |   |   OPEN TCP PORTS    |   | MISSING SECURITY HEADERS|  |  
|  |     3.5 / 10.0      |   |       2 Ports       |   |       3 Headers         |  |  
|  |    (LOW RISK)       |   |     (80, 443\)       |   |   (CSP, HSTS, X-Frame)  |  |  
|  \+---------------------+   \+---------------------+   \+-------------------------+  |  
|                                                                                   |  
|  \[ Tabs: 🌐 Network Ports | 🔒 HTTP Headers | 📜 SSL Audit | 🔎 DNS/WHOIS \]        |  
|  \+-----------------------------------------------------------------------------+  |  
|  | Port | Service | Banner                           | Status                  |  |  
|  | 80   | HTTP    | nginx/1.18.0                     | Open                    |  |  
|  | 443  | HTTPS   | OpenSSL/1.1.1k                   | Open                    |  |  
|  \+-----------------------------------------------------------------------------+  |  
|                                                                                   |  
|  \[ 📥 Export Executive PDF Report \]             \[ 📊 Export Raw Findings (CSV) \]  |  
\+-----------------------------------------------------------------------------------+

