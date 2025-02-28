"""Fake Embedding class for testing purposes."""
from typing import List

from langchain.embeddings.base import Embeddings

fake_texts = ["foo", "bar", "baz"]


class FakeEmbeddings(Embeddings):
    """Fake embeddings functionality for testing."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return simple embeddings.
        Embeddings encode each text as its index."""
        return [[float(1.0)] * 9 + [float(i)] for i in range(len(texts))]

    def _embed_query(self, text: str) -> List[float]:
        """Return simple embeddings."""
        return [float(1.0)] * 9 + [float(0.0)]
