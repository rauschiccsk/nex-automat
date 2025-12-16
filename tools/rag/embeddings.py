"""
RAG Embeddings Module
Handles text embedding generation using sentence-transformers
"""

from typing import List, Optional, Union
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import EmbeddingConfig, get_config


class EmbeddingModel:
    """
    Wrapper for sentence-transformers embedding model

    Handles model loading, caching, and batch embedding generation.
    """

    def __init__(self, config: Optional[EmbeddingConfig] = None):
        """
        Initialize embedding model

        Args:
            config: Embedding configuration, uses global config if None
        """
        if config is None:
            config = get_config().embedding

        self.config = config
        self.model: Optional[SentenceTransformer] = None
        self._dimension: Optional[int] = None

    def load(self) -> None:
        """Load the embedding model"""
        if self.model is not None:
            return  # Already loaded

        print(f"Loading embedding model: {self.config.model_name}")

        # Load model
        self.model = SentenceTransformer(
            self.config.model_name,
            cache_folder=str(self.config.cache_dir) if self.config.cache_dir else None,
            device=self.config.device
        )

        # Set max sequence length
        self.model.max_seq_length = self.config.max_seq_length

        # Verify dimension
        self._dimension = self.model.get_sentence_embedding_dimension()

        if self._dimension != self.config.dimension:
            print(f"Warning: Model dimension {self._dimension} != config dimension {self.config.dimension}")

        print(f"✓ Model loaded (dimension: {self._dimension})")

    def encode(
            self,
            texts: Union[str, List[str]],
            batch_size: Optional[int] = None,
            show_progress: bool = False,
            normalize: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for text(s)

        Args:
            texts: Single text or list of texts
            batch_size: Batch size for processing, uses config default if None
            show_progress: Show progress bar
            normalize: Normalize embeddings to unit length

        Returns:
            Numpy array of embeddings (N x dimension)
        """
        if self.model is None:
            self.load()

        if batch_size is None:
            batch_size = self.config.batch_size

        # Convert single text to list
        single_input = isinstance(texts, str)
        if single_input:
            texts = [texts]

        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=normalize,
            convert_to_numpy=True
        )

        # Return single embedding if single input
        if single_input:
            return embeddings[0]

        return embeddings

    def encode_batch(
            self,
            texts: List[str],
            batch_size: Optional[int] = None,
            show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for batch of texts

        Convenience method that always shows progress and returns array.

        Args:
            texts: List of texts
            batch_size: Batch size for processing
            show_progress: Show progress bar

        Returns:
            Numpy array of embeddings (N x dimension)
        """
        return self.encode(
            texts,
            batch_size=batch_size,
            show_progress=show_progress,
            normalize=True
        )

    @property
    def dimension(self) -> int:
        """Get embedding dimension"""
        if self._dimension is None:
            if self.model is None:
                self.load()
            self._dimension = self.model.get_sentence_embedding_dimension()
        return self._dimension

    @property
    def device(self) -> str:
        """Get device being used"""
        if self.model is None:
            self.load()
        return str(self.model.device)

    def __repr__(self) -> str:
        loaded = "loaded" if self.model is not None else "not loaded"
        return f"EmbeddingModel(model={self.config.model_name}, {loaded})"


# Global model instance (lazy loaded)
_model: Optional[EmbeddingModel] = None


def get_model(reload: bool = False) -> EmbeddingModel:
    """
    Get global embedding model (singleton pattern)

    Args:
        reload: Force reload model

    Returns:
        EmbeddingModel instance
    """
    global _model

    if _model is None or reload:
        _model = EmbeddingModel()
        _model.load()

    return _model


def embed_text(text: str, normalize: bool = True) -> np.ndarray:
    """
    Quick helper to embed single text

    Args:
        text: Text to embed
        normalize: Normalize embedding

    Returns:
        Embedding vector
    """
    model = get_model()
    return model.encode(text, normalize=normalize)


def embed_texts(texts: List[str], batch_size: Optional[int] = None) -> np.ndarray:
    """
    Quick helper to embed multiple texts

    Args:
        texts: List of texts
        batch_size: Batch size

    Returns:
        Array of embeddings
    """
    model = get_model()
    return model.encode_batch(texts, batch_size=batch_size)


if __name__ == "__main__":
    # Test embedding model
    print("Testing embedding model...")

    # Test single text
    text = "This is a test sentence."
    embedding = embed_text(text)
    print(f"✓ Single text embedded: shape={embedding.shape}")

    # Test batch
    texts = [
        "First test sentence.",
        "Second test sentence.",
        "Third test sentence."
    ]
    embeddings = embed_texts(texts)
    print(f"✓ Batch embedded: shape={embeddings.shape}")

    # Test similarity
    similarity = np.dot(embeddings[0], embeddings[1])
    print(f"✓ Similarity (0,1): {similarity:.4f}")