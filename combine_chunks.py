import json
import os

RAW_DOCS_DIR = "raw_docs"
RAW_DOCS_2_DIR = "rawDocs"
OUTPUT_DIR = "docs"

def load_chunks(folder):
    path = os.path.join(folder, "chunks.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    chunks_1 = load_chunks(RAW_DOCS_DIR)
    chunks_2 = load_chunks(RAW_DOCS_2_DIR)

    combined = chunks_1 + chunks_2

    print(f"{RAW_DOCS_DIR}: {len(chunks_1)} chunks")
    print(f"{RAW_DOCS_2_DIR}: {len(chunks_2)} chunks")
    print(f"combined: {len(combined)} chunks")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "chunks.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"saved to {out_path}")

if __name__ == "__main__":
    main()