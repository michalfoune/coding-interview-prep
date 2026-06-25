"""
Mini Search / In-Memory Retrieval Index

Assignment
----------
Implement a small in-memory search engine over a static list of documents.

Input documents have this shape:
    {"id": "doc_id", "text": "document text"}

Requirements
------------
1. Build an inverted index from the documents.
   - Normalize text to lowercase.
   - Tokenize text into word-like tokens.
   - Ignore punctuation.
   - Ignore duplicate tokens within the same document.

2. Implement search_with_scores(query, k).
   - Normalize/tokenize the query using the same tokenizer.
   - Ignore duplicate query tokens.
   - Score each document by the number of unique query tokens it contains.
   - Do not return documents with score 0.
   - Sort by score descending, then document ID ascending.
   - Return at most k results as (doc_id, score) tuples.

3. Implement search(query, k).
   - Return only document IDs, using search_with_scores as the core implementation.

Edge cases covered
------------------
- Empty query or missing query tokens.
- Repeated query tokens.
- Punctuation and case differences.
- k <= 0.
- k larger than the number of matching documents.
- No matching documents.
"""

import re
from collections import defaultdict


class InvertedSearchIndex:
    def __init__(self, documents: list[dict[str, str]]):
        self.inverted_index: dict[str, set[str]] = defaultdict(set)

        for document in documents:
            doc_id = document["id"]
            tokens = set(self._tokenize(document["text"]))

            for token in tokens:
                self.inverted_index[token].add(doc_id)

    def _tokenize(self, text: str) -> list[str]:
        if not text:
            return []

        text = text.strip().lower()
        return re.findall(
            r"\b[a-z0-9]+\b",
            text,
        )

    def search_with_scores(self, query: str, k: int) -> list[tuple[str, int]]:
        if k <= 0:
            return []

        keywords = set(self._tokenize(query))
        candidate_scores: dict[str, int] = defaultdict(int)

        for keyword in keywords:
            docs = self.inverted_index.get(keyword, set())
            for doc_id in docs:
                candidate_scores[doc_id] += 1

        sorted_docs = sorted(
            candidate_scores.items(),
            key=lambda item: (-item[1], item[0]),
        )

        return sorted_docs[:k]

    def search(self, query: str, k: int) -> list[str]:
        return [doc_id for doc_id, _ in self.search_with_scores(query, k)]


def main():
    docs = [
        {
            "id": "Python the Snake",
            "text": "Python is the language where the snake is in the name.",
        },
        {
            "id": "Java The Legacy",
            "text": """Java is the language I started with. It was a great entry point into programming, but compared with Python it now feels much more verbose.""",
        },
    ]

    search_index = InvertedSearchIndex(docs)

    assert search_index.search("snake", 2) == ["Python the Snake"]
    assert search_index.search("python python", 2) == ["Python the Snake"]
    assert search_index.search("oracle java", 1) == ["Java The Legacy"]
    assert search_index.search("python", 0) == []
    assert search_index.search("missing", 1) == []
    assert search_index.search("PYTHON!!!", 2) == ["Python the Snake"]
    assert search_index.search("is", 2) == ["Java The Legacy", "Python the Snake"]
    assert search_index.search_with_scores("snake", 2) == [("Python the Snake", 1)]

    print("All tests passed.")


if __name__ == "__main__":
    main()
