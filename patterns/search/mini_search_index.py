#########################################################
## This is not my work -- this is a generated solution ##
#########################################################


import re
from collections import defaultdict, Counter


class MiniSearchIndex:
    """
    Simple in-memory keyword search index.

    Supports:
    - adding documents by doc_id
    - tokenizing text
    - building an inverted index: token -> set(doc_id)
    - searching by query terms
    - ranking documents by number of matched query terms

    This is a simplified RAG-like retrieval component:
    query -> candidate documents -> ranked results.
    """

    def __init__(self):
        self.documents: dict[str, str] = {} # book_name -> raw_body_text
        self.doc_tokens: dict[str, Counter[str]] = {} # book_name -> freqency of keywords
        self.index: dict[str, set[str]] = defaultdict(set) # keyword -> set of book names

    def _tokenize(self, text: str) -> list[str]:
        """
        Convert text into normalized tokens.

        Example:
            "API failed, API timeout!" -> ["api", "failed", "api", "timeout"]
        """
        return re.findall(r"\b[a-z0-9]+\b", text.lower())

    def add_document(self, doc_id: str, text: str) -> None:
        """
        Add or replace a document.

        If doc_id already exists, remove its old tokens from the index first.
        """
        if doc_id in self.documents:
            self._remove_document_from_index(doc_id)

        tokens = self._tokenize(text)

        self.documents[doc_id] = text
        self.doc_tokens[doc_id] = Counter(tokens)

        for token in self.doc_tokens[doc_id]:
            self.index[token].add(doc_id)

    def _remove_document_from_index(self, doc_id: str) -> None:
        """Remove an existing document's tokens from the inverted index."""
        old_tokens = self.doc_tokens.get(doc_id, {})

        for token in old_tokens:
            self.index[token].discard(doc_id)

            if not self.index[token]:
                del self.index[token]

        self.documents.pop(doc_id, None)
        self.doc_tokens.pop(doc_id, None)

    def search(self, query: str, limit: int = 5) -> list[tuple[str, int]]:
        """
        Return matching documents ranked by score.

        Score:
        - For each query token, add the token frequency in the document.
        - Higher score ranks first.
        - Ties are broken alphabetically by doc_id.

        Returns:
            list of (doc_id, score)
        """
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        scores = defaultdict(int)

        for token in query_tokens:
            candidate_docs = self.index.get(token, set())

            for doc_id in candidate_docs:
                scores[doc_id] += self.doc_tokens[doc_id][token]

        ranked_results = sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0]),
        )

        return ranked_results[:limit]


def main():
    index = MiniSearchIndex()

    index.add_document(
        "doc1",
        "API service failed because of database timeout",
    )
    index.add_document(
        "doc2",
        "Database migration completed successfully",
    )
    index.add_document(
        "doc3",
        "Worker service retried after API timeout",
    )
    index.add_document(
        "doc4",
        "Frontend checkout page loaded successfully",
    )

    assert index.search("api timeout") == [
        ("doc1", 2),
        ("doc3", 2),
    ]

    assert index.search("database") == [
        ("doc1", 1),
        ("doc2", 1),
    ]

    assert index.search("successfully") == [
        ("doc2", 1),
        ("doc4", 1),
    ]

    assert index.search("missing term") == []

    # Replacing an existing document should remove its old indexed tokens.
    index.add_document(
        "doc1",
        "Authentication service failed",
    )

    assert index.search("database timeout") == [
        ("doc2", 1),
        ("doc3", 1),
    ]

    assert index.search("authentication") == [
        ("doc1", 1),
    ]

    print("All tests passed.")


if __name__ == "__main__":
    main()