import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Opens a PDF and extracts all text from every page.
    Returns a single cleaned string.
    """
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text: 
                full_text += f"\n--- Page {page_number} ---\n"
                full_text += text

    return full_text.strip()


# Test it
if __name__ == "__main__":
    pdf_path = r"files/CBC-test-report.pdf"
    extracted = extract_text_from_pdf(pdf_path)

    print(f"Total characters extracted: {len(extracted)}")
    print("\n--- PREVIEW (first 500 chars) ---\n")
    print(extracted[:500])
    # Rough token estimate (1 token ≈ 4 characters)
    estimated_tokens = len(extracted) / 4
    print(f"\nEstimated tokens: {estimated_tokens:.0f}")
    print(f"Gemini 1.5 Flash limit: 1,000,000 tokens")
    print(f"Safe to send? {' Yes' if estimated_tokens < 900000 else ' Too large'}")