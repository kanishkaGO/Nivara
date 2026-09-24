# Nivara
NIVARA is an autonomous multi-agent AI system designed to bridge the employment gap for Persons with Disabilities (PwDs). It matches candidates not just on technical skills, but on precise physical infrastructure, assistive software compatibility, and workplace accommodation requirements.
# ♿ Nivara: Agentic Inclusive Career & Accommodation Matcher

> An autonomous multi-agent system designed to bridge the accessibility gap in hiring for Persons with Disabilities (PwDs) by aligning technical competencies with digital and physical workplace accommodations.

---

## 📌 Problem Statement

Traditional job platforms match candidates solely on resume keywords and prior experience. For candidates with disabilities, critical operational factors are routinely overlooked:
- **Opaque Workplace Infrastructure:** Job postings rarely disclose wheelchair accessibility, screen-reader software compliance, sensory-friendly environments, or adaptive tooling.
- **Complex UI Barriers:** Multi-step job applications, non-standard form controls, and bloated portals create friction for assistive-tech and motor-impaired users.
- **Post-Hire Accommodation Friction:** Candidates often face disclosure anxiety or discover only after being hired that the company cannot support their required accommodations.

---

## 💡 Solution Overview

**Nivara** replaces manual keyword filtering with an autonomous three-tier agent pipeline. A candidate provides minimal natural input (a voice transcript or simple bio), and specialized agents extract skills, audit listings, evaluate infrastructure readiness, and draft accommodation proposals.

              [Candidate Input: Natural Bio / Voice]
                                 │
                                 ▼
    ┌────────────────────────────────────────────────────────┐
    │             1. Candidate Advocate Agent                │
    │  • Extracts technical stack and experience             │
    │  • Maps functional accommodations & assistive needs    │
    └────────────────────────────┬───────────────────────────┘
                                 │
                                 ▼ (Structured Profile)
    ┌────────────────────────────────────────────────────────┐
    │           2. Workplace & Job Auditor Agent             │
    │  • Ingests job database and evaluates company policies │
    │  • Disqualifies roles with conflicting constraints     │
    └────────────────────────────┬───────────────────────────┘
                                 │
                                 ▼ (Vetted Opportunities)
    ┌────────────────────────────────────────────────────────┐
    │       3. Accommodation Matcher & Pitch Agent           │
    │  • Computes Accessibility Compatibility Score (%)      │
    │  • Generates an actionable Employer Onboarding Brief   │
    └────────────────────────────────────────────────────────┘

---

## 🛠️ Architecture & Multi-Agent Design

| Agent Name | Role | Core Responsibility |
| :--- | :--- | :--- |
| **Candidate Advocate Agent** | Needs Assessor | Translates natural, conversational input into structured technical competencies and physical/digital workplace requirements (e.g., NVDA screen reader, ergonomic input hardware, remote-only). |
| **Job Auditor Agent** | Policy & Culture Evaluator | Evaluates job postings against candidate constraints, discarding roles with mandatory on-site policies or inaccessible internal toolchains. |
| **Accommodation Matcher Agent** | Solution Broker | Computes the final compatibility score, details the gap analysis, and generates an onboarding proposal for hiring managers. |

---

## 💻 Tech Stack

- **LLM Engine:** Google Gemini API (`gemini-1.5-flash` / `gemini-1.5-pro`)
- **Agent Orchestration:** CrewAI / LangChain
- **Frontend / UI:** Streamlit (Clean, high-contrast, accessible design)
- **Language:** Python 3.10+

---

## 📂 Project Structure

```text
Nivara/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── app.py                     # Streamlit frontend dashboard
├── src/
│   ├── __init__.py
│   ├── agents.py              # CrewAI agent definitions
│   ├── tasks.py               # Agent task descriptions & expected outputs
│   └── mock_jobs.py           # Sample job listings with accessibility tags
└── assets/
    └── architecture_flow.png  # System architecture diagram
