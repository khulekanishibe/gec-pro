import sys
import json
import language_tool_python
import spacy
from spacy.matcher import Matcher
import os
import re
import math
from collections import Counter

# --- CONFIGURATION & THRESHOLDS ---
BURSTINESS_THRESHOLD = 8.0
ENTROPY_THRESHOLD = 6.5
DEFAULT_DIALECT = 'en-GB'

# --- GLOBAL RESOURCE CACHE (Lazy Loading) ---
_NLP_MODEL = None
_LANG_TOOL = None

def get_nlp():
    global _NLP_MODEL
    if _NLP_MODEL is None:
        try:
            _NLP_MODEL = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError("SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    return _NLP_MODEL

def get_lang_tool(lang):
    global _LANG_TOOL
    if _LANG_TOOL is None or _LANG_TOOL.language.tag != lang:
        try:
            _LANG_TOOL = language_tool_python.LanguageTool(lang)
        except Exception as e:
            if "java" in str(e).lower():
                raise RuntimeError("Java not found or incompatible. LanguageTool requires Java 17+. Run 'java -version' to check.")
            raise e
    return _LANG_TOOL

def calculate_ai_markers(doc):
    """Calculates statistical markers to predict AI vs Human authorship."""
    sentences = list(doc.sents)
    lengths = [len(sent) for sent in sentences]
    
    if not lengths: 
        return {"burstiness_score": 0, "entropy_score": 0, "prediction": "Unknown", "confidence": "None"}
    
    # 1. Burstiness: Standard Deviation of sentence lengths
    avg_len = sum(lengths) / len(lengths)
    variance = sum((x - avg_len) ** 2 for x in lengths) / len(lengths)
    burstiness = math.sqrt(variance)
    
    # 2. Perplexity Proxy (Shannon Entropy)
    words = [token.text.lower() for token in doc if token.is_alpha]
    if not words: 
        return {"burstiness_score": round(burstiness, 2), "entropy_score": 0, "prediction": "Likely AI", "confidence": "Low"}
    
    counts = Counter(words)
    total = len(words)
    entropy = -sum((count/total) * math.log2(count/total) for count in counts.values())
    
    # Classification logic
    is_human = (burstiness > BURSTINESS_THRESHOLD) and (entropy > ENTROPY_THRESHOLD)
    
    # Confidence Level
    confidence = "High" if len(sentences) >= 5 else "Low (Sample size too small)"
    
    return {
        "burstiness_score": round(burstiness, 2),
        "entropy_score": round(entropy, 2),
        "prediction": "Likely Human" if is_human else "Likely AI-Generated/Highly Uniform",
        "confidence": confidence
    }

def check_text(text, lang=DEFAULT_DIALECT):
    results = {
        "mechanical_errors": [],
        "structural_issues": [],
        "style_and_tone": [],
        "authorship_audit": {},
        "summary": {}
    }
    
    # 1. Resource Initialization
    try:
        nlp = get_nlp()
        tool = get_lang_tool(lang)
    except RuntimeError as e:
        return {"error": str(e)}

    # 2. Deep Analysis (SpaCy)
    doc = nlp(text)
    results["authorship_audit"] = calculate_ai_markers(doc)
    
    matcher = Matcher(nlp.vocab)
    matcher.add("PASSIVE_VOICE", [[{"DEP": "auxpass"}, {"DEP": "ROOT", "TAG": "VBN"}]])
    matcher.add("SPLIT_INFINITIVE", [[{"LOWER": "to"}, {"POS": "ADV"}, {"POS": "VERB"}]])
    matcher.add("ACADEMIC_CONJUNCTION", [[{"TEXT": {"IN": ["But", "And", "So"]}, "IS_SENT_START": True}]])
    
    hedging_words = ["basically", "actually", "just", "maybe", "perhaps", "potentially", "I think"]
    for word in hedging_words:
        matcher.add("HEDGING_WEAKNESS", [[{"LOWER": word}]])

    # 3. Execution Pass
    # Mechanical (LanguageTool)
    matches = tool.check(text)
    for match in matches:
        results["mechanical_errors"].append({
            "message": match.message,
            "replacements": match.replacements[:3],
            "offset": match.offset,
            "length": match.error_length,
            "rule_id": match.rule_id,
            "context": match.context
        })

    # Structural & Tone (Matchers)
    spacy_matches = matcher(doc)
    for match_id, start, end in spacy_matches:
        rule_name = nlp.vocab.strings[match_id]
        span = doc[start:end]
        target = results["style_and_tone"] if "HEDGING" in rule_name else results["structural_issues"]
        target.append({"type": rule_name, "text": span.text, "offset": span.start_char})

    # Sentence Length
    for sent in doc.sents:
        if len(sent) > 25:
            results["structural_issues"].append({
                "type": "LONG_SENTENCE",
                "text": sent.text[:60] + "...",
                "message": "Sentence too long (>25 words). Split for clarity."
            })

    results["summary"] = {
        "mechanical": len(results["mechanical_errors"]),
        "structural": len(results["structural_issues"]),
        "style": len(results["style_and_tone"]),
        "ai_prediction": results["authorship_audit"]["prediction"],
        "dialect": lang
    }
    return results

if __name__ == "__main__":
    import os
    import pdfplumber
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No text provided"}))
        sys.exit(1)
    
    input_arg = sys.argv[1]
    input_text = ""
    
    if os.path.isfile(input_arg):
        if input_arg.lower().endswith('.pdf'):
            try:
                with pdfplumber.open(input_arg) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text: input_text += page_text + "\n"
            except Exception as e:
                print(json.dumps({"error": f"Failed to read PDF: {str(e)}"}))
                sys.exit(1)
        else:
            try:
                with open(input_arg, 'r', encoding='utf-8', errors='ignore') as f:
                    input_text = f.read()
            except Exception as e:
                print(json.dumps({"error": f"Failed to read file: {str(e)}"}))
                sys.exit(1)
    else:
        input_text = input_arg
        
    language = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DIALECT
    
    try:
        report = check_text(input_text, language)
        print(json.dumps(report, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
