# AI Agent Instructions for `gec-pro` Skill

## 1. Objective

The `gec-pro` skill provides a private, local, and robust audit of a given text for mechanical errors, structural issues, and stylistic patterns common in AI-generated writing. It is specifically tuned for **British English (en-GB)**.

## 2. Core Workflow: "Audit then Act"

This is a two-phase skill. You **MUST** execute both phases in order.

### Phase 1: Execute the Technical Audit

Your first action is to run the `engine.py` script. The script can accept either a direct file path or a raw text string as its first argument.

**Usage:**
```bash
python /path/to/engine.py "/path/to/document.txt"
```

The script will print a **JSON object** to standard output. This JSON is the "source of truth" for all findings. You must capture and parse this JSON object in memory. **Do not** present this raw JSON to the user.

**JSON Schema:**
```json
{
  "mechanical_errors": [ { "message": "...", "replacements": ["..."], "offset": "...", "length": "...", "sentence": "..." } ],
  "structural_issues": [ { "type": "...", "text": "...", "sentence": "..." } ],
  "style_and_tone": [ { "type": "HEDGING_WEAKNESS", "text": "...", "sentence": "..." } ],
  "ai_cliche_flags": [ { "phrase": "...", "suggestion": "...", "sentence": "..." } ],
  "authorship_audit": { "prediction": "Likely Human", "confidence": "High" },
  "summary": { "mechanical": "...", "structural": "...", "style": "...", "cliches": "..." }
}
```

### Phase 2: Present the "Review Mode" Report

Your second action is to parse the JSON report and present a formatted, human-friendly summary to the user. This is the **"Review Mode"**.

**Critical Interpretation Logic:**
- **IGNORE PROPER NOUNS:** If a `mechanical_error` flags a proper noun (e.g., a name like "GreenFields" or a technical term like "agritech"), inform the user that it is being ignored.
- **ENFORCE BRITISH ENGLISH:** The engine is pre-configured to filter out suggestions to change `-ise` spellings to `-ize`. You do not need to handle this. The engine does it for you.
- **FOCUS ON HIGH-IMPACT ERRORS:** Prioritize presenting clear spelling mistakes, passive voice, long sentences, and AI clichés.

**Report Template:**
For each valid finding, format your output to the user exactly like this:

> #### Category Name (X found)
> *   **Issue:** [Brief description from `message` or `type`]
> *   **Original:**
>     > [The full `sentence` containing the error, with the error text in **bold**.]
> *   **Suggestion:**
>     > [The full `sentence` with the suggested change, also in **bold**.]
>     > *(Rationale: Add a brief explanation for why the change is an improvement, especially for style and clarity issues.)*

### Phase 3: Act on User Feedback

After presenting the "Review Mode" report, you **MUST** ask the user for confirmation before applying any changes.
- **If approved:** Generate a new version of the full text with the approved fixes.
- **If denied:** Discard the suggestions and await further instructions.
