# GEC-Pro: Professional Grammar & Style Engine

A private, local hybrid grammar engine designed to perform technical audits of academic and professional text.

## ⚙️ Setup

### 1. System Tools
- **Java 17+**: Required for the LanguageTool engine.
- **Pandoc**: Required for processing Microsoft Word (`.docx`) files.

You can install both using Chocolatey:
```bash
choco install openjdk17 pandoc -y
```

### 2. Python Environment
Install the required libraries and the NLP model:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 🚀 How to Use

Run the audit on any text or supported file (PDF, TXT, MD):
```bash
python engine.py "C:\path\to\your\document.pdf"
```

## 🛠 Features

- **Mechanical Check**: Comprehensive spelling and punctuation audit via LanguageTool.
- **Structural Linting**: Detects passive voice, split infinitives, and overly long sentences.
- **AI Authorship Markers**: Uses Burstiness and Perplexity metrics to provide statistical markers for human vs. AI writing.
- **Dialect Native**: Pre-configured for British English.

## 🔍 Troubleshooting

- **Java Errors**: If you see "Java not found", ensure OpenJDK 17 is installed and restart your terminal.
- **DOCX Issues**: If Word documents fail to load, verify that `pandoc` is accessible in your terminal.
