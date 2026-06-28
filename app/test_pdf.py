from pdf_loader import load_pdf

text = load_pdf(
    "data/pdfs/test.pdf"
)

print(text[:2000])