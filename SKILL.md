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
  - *Install:* `choco install openjdk17 -y`
- **Pandoc:** Required for extracting text from `.docx` files.
  - *Install:* `choco install pandoc -y`

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
```bash
python C:\Users\yondi\.gemini\skills\gec-pro\engine.py "path/to/your/document.pdf"
```

## 📊 Core Capabilities

- **Mechanical Audit:** Detects typos, punctuation errors, and basic grammar issues using LanguageTool.
- **Structural Analysis:** Identifies passive voice, split infinitives, and overly long sentences using SpaCy.
- **Authorship Statistics:** Provides statistical markers (sentence "burstiness" and vocabulary "entropy") to help distinguish between human and AI-generated writing.
- **Dialect Enforcement:** Strictly tuned for **British English** (Oxford/UK standards).

## 💡 Troubleshooting

- **"Java not found":** Ensure Java 17+ is installed and your terminal has been restarted to refresh environment variables.
- **"Match object has no attribute 'suggestions'":** This was a known bug in older versions of the skill. Ensure you are using the latest `engine.py` which uses `match.replacements`.
- **".docx files not reading":** Ensure `pandoc` is installed. The agent uses pandoc to convert `.docx` to a readable format before auditing.

## 🔄 Workflow
1.  **Run Audit:** The agent calls the engine to generate a JSON report.
2.  **Review & Apply:** The agent (I) will then parse this report and help you rewrite or polish the text based on the findings.
