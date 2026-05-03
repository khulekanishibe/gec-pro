# GEC-Pro: A Private, Local Grammar & Style Engine

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

**GEC-Pro is a private, local, hybrid grammar engine designed for academic and professional writing. It provides a detailed technical audit of your text, focusing on British English standards, structural integrity, and authorship analysis without ever sending your data to an external cloud service.**

This tool was created to provide a powerful, privacy-first alternative to commercial grammar checkers, with special features tailored for academic use.

---

## ✨ Key Features

*   **🔒 100% Local & Private:** Your text is processed entirely on your machine. Nothing is ever uploaded to a third-party service.
*   **🇬🇧 British English Native:** Strictly enforces UK/Oxford spelling, grammar, and punctuation conventions. Automatically filters out incorrect suggestions (like American "-ize" spellings).
*   **🎓 Academic & Structural Analysis:** Uses `spaCy` to perform deep linguistic analysis, identifying passive voice, split infinitives, and overly long or complex sentences that hinder readability.
*   **🤖 Dual AI Detection Engine:**
    1.  **Statistical Analysis:** Measures sentence "burstiness" and vocabulary "entropy" to determine if the writing *feels* robotic.
    2.  **Lexical Analysis:** Detects and flags common AI-generated cliché phrases (e.g., "in the digital landscape," "it is important to note that...").
*   **⚙️ Rule-Based Mechanical Audit:** Leverages the power of `LanguageTool` to find thousands of pattern-based errors in spelling, punctuation, and grammar.

---

## 🚀 "Review Mode" in Action

`gec-pro` doesn't just fix your text; it helps you understand the issues. When run by an AI agent, it produces a clear, actionable report.

#### **Before (The Engine's Raw JSON Output):**
```json
{
  "message": "This sentence appears to be written in the passive voice.",
  "offset": 2365, "length": 10, "rule_id": "PASSIVE_VOICE",
  "sentence": "Currently, the bookstore's operational model is defined by a complete reliance on manual workflows..."
}
```

#### **After (The Agent's "Review Mode" Report):**
> ### Structural Issues (1)
> *   **Issue:** Passive Voice
> *   **Original:**
>     > Currently, the bookstore's operational model **is defined** by a complete reliance on manual workflows and basic spreadsheet applications...
> *   **Suggestion:**
>     > Currently, a complete reliance on manual workflows and basic spreadsheet applications **defines** the bookstore's operational model...

---

## 🛠️ Prerequisites & Setup

### 1. System Requirements
*   **Java 17+:** Required by the LanguageTool engine.
*   **Pandoc:** (Optional) Required for processing Microsoft Word (`.docx`) files.

On Windows, you can install both easily using Chocolatey:
```bash
choco install openjdk17 pandoc -y
```

### 2. Python Environment
This project uses the Python packages listed in `requirements.txt`.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Download the NLP model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

## 🚀 Usage

The engine can be run directly from the command line on a text file, PDF, or raw string.

```bash
# Example: Auditing a PDF file
python engine.py "C:\path	o\your\document.pdf"
```

When used as an AI agent skill, the agent will handle this execution for you.

## 💡 Troubleshooting

*   **"Java not found":** Ensure Java 17+ is installed and that you have restarted your terminal session to update the system's PATH environment variable.
*   **`.docx` file errors:** Ensure `pandoc` is installed and accessible from your terminal.

---
*This skill was developed as a demonstration of building powerful, local, and private AI-native tools.*
