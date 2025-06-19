import sys
from pypdf import PdfReader

def extract_text_per_page(path):
    reader = PdfReader(path)
    return [page.extract_text().lower() if page.extract_text() else "" for page in reader.pages]

'''if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_extractor.py <filename.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        pages_text = extract_text_per_page(pdf_path)
        
    except FileNotFoundError:
        print(f"Error: File '{pdf_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")'''