"""Wrapper around TensorflowHub embedding models."""
from typing import Any, List

from pydantic import Extra

from langchain.embeddings.base import Embeddings

DEFAULT_MODEL_URL = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"


class TensorflowHubEmbeddings(Embeddings):
    """Wrapper around tensorflow_hub embedding models.

    To use, you should have the ``tensorflow_text`` python package installed.

    Example:
        .. code-block:: python

            from langchain.embeddings import TensorflowHubEmbeddings
            url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
            tf = TensorflowHubEmbeddings(model_url=url)
    """

    embed: Any  #: :meta private:
    model_url: str = DEFAULT_MODEL_URL
    """Model name to use."""

    def __init__(self, **kwargs: Any):
        """Initialize the tensorflow_hub and tensorflow_text."""
        super().__init__(**kwargs)
        try:
            import tensorflow_hub
            import tensorflow_text  # noqa

            self.embed = tensorflow_hub.load(self.model_url)
        except ImportError as e:
            raise ValueError(
                "Could not import some python packages." "Please install them."
            ) from e

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a TensorflowHub embedding model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.embed(texts).numpy()
        return embeddings.tolist()

    def _embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a TensorflowHub embedding model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        text = text.replace("\n", " ")
        embedding = self.embed(text).numpy()[0]
        return embedding.tolist()
