---
name: gec-pro
description: |
  A local GEC engine for British English that provides a detailed audit of mechanical errors, structural issues, and statistical markers for AI authorship.
---

# GEC-Pro: Local Grammar Engine

GEC-Pro is a private, local hybrid grammar engine that provides a detailed technical audit of a text, focusing on British English standards.

## 🛠 Prerequisites & Setup

This skill requires specific system tools and Python libraries to function.

### 1. System Requirements
- **Java 17+:** Required by the LanguageTool engine.
  - *Install (Windows, via Chocolatey):* `choco install openjdk17 -y`

### 2. Python Dependencies
Run these commands from your terminal to install the necessary libraries:
```bash
# Install Python packages
pip install language-tool-python spacy pdfplumber

# Download the NLP model
python -m spacy download en_core_web_sm
```

## 🚀 Usage

You can audit raw text, `.txt` files, `.md` files, or `.pdf` files directly.

### Audit Command

To run from anywhere:
```bash
# Use the full path to the script and your document
python C:\Users\yondi\.gemini\skills\gec-pro\engine.py "C:\path\to\my\document.pdf"
```

Or, from inside the skill directory:
```bash
cd C:\Users\yondi\.gemini\skills\gec-pro
python engine.py "C:\path\to\my\document.pdf"
```

## 📊 Core Capabilities

- **Mechanical Audit:** Detects typos, punctuation errors, and basic grammar issues using LanguageTool.
- **Structural Analysis:** Identifies passive voice, split infinitives, and overly long sentences using SpaCy.
- **Authorship Statistics:** Provides statistical markers (sentence "burstiness" and vocabulary "entropy") to help distinguish between human and AI-generated writing.
- **Dialect Enforcement:** Strictly tuned for **British English** (Oxford/UK standards). The engine automatically ignores OED-style "-ize" suggestions to enforce common "-ise" spelling.

## 💡 Troubleshooting

- **"Java not found":** Ensure Java 17+ is installed and your terminal has been restarted to refresh environment variables.
- **"Match object has no attribute 'suggestions'":** This was a known bug in older versions of the skill. Ensure you are using the latest `engine.py` which uses `match.replacements`.

## 🔄 Workflow: Audit then Act

This skill uses a two-phase process to give you maximum control.

### Phase 1: Technical Audit
First, the agent runs the `engine.py` script on your text. This produces a detailed, private JSON report of all potential issues without making any changes to your document. This report is the "single source of truth" for all findings.

### Phase 2: Agent-Led Review
The agent can then parse the technical JSON report and present it to you in a human-friendly "Review Mode". This is an interactive process driven by the agent, not a feature of the script itself. For each issue, the agent will show:
- **The Category:** (e.g., Mechanical, Structural, Style)
- **The Original Sentence:** The full sentence containing the issue.
- **The Suggested Change:** A clear "before and after" comparison.

```
### Mechanical Errors (1)

*   **Issue:** Spelling ("buisness")
*   **Original:** The core of our buisness is customer satisfaction.
*   **Suggestion:** The core of our business is customer satisfaction.
```

You can then decide which changes to apply, ensuring the final text maintains your voice and intent.
