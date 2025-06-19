from clauses import CLAUSES
from thefuzz import fuzz


def match_phrases(page_text, phrases, threshold=80):
    matches = []
    for phrase in phrases:
        for sentence in page_text.split("."):
            score = fuzz.partial_ratio(phrase, sentence.strip())
            if score >= threshold:
                matches.append((phrase, sentence.strip(), score))
    return matches

def evaluate_clause_on_page(page_text, clause_data):
    pos_matches = match_phrases(page_text, clause_data["positive"])
    neg_matches = match_phrases(page_text, clause_data["negative"])
    return pos_matches, neg_matches

def evaluate_all_clauses(pages):
    results = {clause: {"positive": [], "negative": []} for clause in CLAUSES}

    for page_num, text in enumerate(pages, start=1):
        for clause, data in CLAUSES.items():
            pos, neg = evaluate_clause_on_page(text, data)
            if pos:
                results[clause]["positive"].append((page_num, pos))
            if neg:
                results[clause]["negative"].append((page_num, neg))

    return results
