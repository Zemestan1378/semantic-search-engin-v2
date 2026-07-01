import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "data", "pdfs")

PDFS = {
    "t1.pdf": "https://raw.githubusercontent.com/Zemestan1378/semantic-search-engin/main/data/pdfs/t1.pdf",
    "t2.pdf": "https://raw.githubusercontent.com/Zemestan1378/semantic-search-engin/main/data/pdfs/t2.pdf",
    "t3.pdf": "https://raw.githubusercontent.com/Zemestan1378/semantic-search-engin/main/data/pdfs/t3.pdf",
}

os.makedirs(PDF_DIR, exist_ok=True)

for filename, url in PDFS.items():
    path = os.path.join(PDF_DIR, filename)

    if os.path.exists(path):
        print(f"{filename} already exists.")
        continue

    print(f"Downloading {filename}...")

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    with open(path, "wb") as f:
        f.write(r.content)

print("All PDFs downloaded.")