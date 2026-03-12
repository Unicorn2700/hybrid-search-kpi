from pathlib import Path
import random


topics = [
    "machine learning",
    "artificial intelligence",
    "data science",
    "python programming",
    "neural networks",
    "deep learning",
    "search engines",
    "information retrieval",
    "cloud computing",
    "databases"
]


def generate_docs(n=300):

    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    for i in range(n):

        topic = random.choice(topics)

        text = f"""
        Document {i} discusses {topic}.
        {topic} is an important field in modern technology.
        Many systems rely on {topic} for intelligent decision making.
        """

        with open(raw_dir / f"doc_{i}.txt", "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    generate_docs()