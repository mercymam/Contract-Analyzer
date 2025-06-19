
from pdf_extracter import extract_text_per_page
from process_extracted_tenancy import evaluate_all_clauses

def print_report(clause_results):
    print("\n📋 Tenant-Friendliness Clause Report\n")

    for clause, data in clause_results.items():
        pos = data["positive"]
        neg = data["negative"]
        if pos and not neg:
            status = "✅ Favourable"
        elif neg and not pos:
            status = "❌ Unfavourable"
        elif pos and neg:
            status = "⚠️ Mixed"
        else:
            status = "❌ Missing"

        print(f"{clause}: {status}")
        if pos:
            for page, matches in pos:
                for _, sentence, score in matches:
                    print(f"  ✅ Page {page} → {sentence} (Score {score})")
        if neg:
            for page, matches in neg:
                for _, sentence, score in matches:
                    print(f"  ❌ Page {page} → {sentence} (Score {score})")
        print("-" * 60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python tenant_clause_evaluator.py <agreement.pdf>")
    else:
        pdf_path = sys.argv[1]
        print(f"\n🔍 Scanning tenancy agreement: {pdf_path}\n")
        pages = extract_text_per_page(pdf_path)
        results = evaluate_all_clauses(pages)
        print_report(results)


