import argparse
import json
from pathlib import Path
from datetime import datetime


def clean_text(text: str) -> str:
    return " ".join(text.split())


def ingest_documents(input_dir: str, output_file: str):

    input_path = Path(input_dir)
    output_path = Path(output_file)

    docs = []
    doc_id = 0

    for file in input_path.glob("*"):

        if file.suffix not in [".txt", ".md"]:
            continue

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        text = clean_text(text)

        doc = {
            "doc_id": doc_id,
            "title": file.stem,
            "text": text,
            "source": str(file),
            "created_at": datetime.utcnow().isoformat()
        }

        docs.append(doc)
        doc_id += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc) + "\n")

    print(f"Ingested {len(docs)} documents → {output_file}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Input directory containing documents"
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output JSONL file"
    )

    args = parser.parse_args()

    ingest_documents(args.input, args.out)


if __name__ == "__main__":
    main()