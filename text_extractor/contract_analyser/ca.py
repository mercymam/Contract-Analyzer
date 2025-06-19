import sys
import re
from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    """
    Extract all text from a PDF file.
    """

    reader = PdfReader(file_path)
    #final_output = "Favourable to Tenant ✅"
    for page in reader.pages:
        text = page.extract_text()
        if "Ending Tenancy" in text:
            return find_key_notice_info(text)    
        else :
            continue
    print(" ")
    return "Program finished"
    
    
def find_key_notice_info(pdf_page):
    reasons = []

    text = pdf_page
    
   # Clean up line breaks between words and numbers
    clean_text = re.sub(r'\s+', ' ', text)
   
    # Extract notice periods
    tenant_match = re.search(r'Tenant.*?minimum of (\d+)\s*month', clean_text, re.IGNORECASE)
    landlord_match = re.search(r'Landlord.*?minimum of (\d+)\s*months?', clean_text, re.IGNORECASE | re.DOTALL)

    tenant_notice = int(tenant_match.group(1)) if tenant_match else None

    landlord_notice_match = re.search(
            r'Landlord must serve a minimum of (\d+)\s*months?', clean_text, re.IGNORECASE)
    landlord_notice = int(landlord_notice_match.group(1)) if landlord_notice_match else None

    #print(f"--tenant notice: {tenant_notice} and landlord notice: {landlord_notice}")

     # Favourability check based on notice periods
    if tenant_notice is not None and landlord_notice is not None:
        if tenant_notice < landlord_notice:
                reasons.append(f"Tenant notice period ({tenant_notice} month) is shorter than landlord's ({landlord_notice} months).")
        elif tenant_notice > landlord_notice:
                reasons.append(f"Tenant notice period ({tenant_notice} months) is longer than landlord's ({landlord_notice} months).")
        else:
                reasons.append("Tenant and landlord have equal notice periods, which is fair.")

     # Check for penalty mentions
    if re.search(r're-letting fees?|penalt(y|ies)|losses caused', clean_text, re.IGNORECASE):
        reasons.append("Clause includes potential financial penalties or re-letting fees.")

    # Check for minimum term lock-in
    if re.search(r'not (?:.*)?within the first (\d+)\s*months?', clean_text, re.IGNORECASE):
        reasons.append("Break clause cannot be used within the initial fixed term period.")

    # Summary logic
    if tenant_notice is None or landlord_notice is None:
        return "Cannot determine (missing notice info)", reasons

    if tenant_notice <= landlord_notice and not any('penalty' in r.lower() for r in reasons):
        return "Favourable to Tenant ✅", reasons
    else:
        return "Unfavourable to Tenant ❌", reasons
    
    


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tenant_clause_evaluator.py <agreement.pdf>")
    else:
        pdf_path = sys.argv[1]
        status, explanation = extract_text_from_pdf(pdf_path)
        print(status)
    for reason in explanation:
        print("•", reason)