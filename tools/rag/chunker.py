"""
RAG Chunker Module
Document chunking utilities for semantic text splitting
"""

from typing import List, Optional
import tiktoken

from .config import ChunkingConfig, get_config


class DocumentChunker:
    """
    Handles document chunking with overlap

    Splits documents into chunks of approximately equal token count
    with configurable overlap for context preservation.
    """

    def __init__(self, config: Optional[ChunkingConfig] = None):
        """
        Initialize document chunker

        Args:
            config: Chunking configuration, uses global config if None
        """
        if config is None:
            config = get_config().chunking

        self.config = config

        # Initialize tokenizer for accurate token counting
        # Using cl100k_base (GPT-4 tokenizer) as good general purpose tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text

        Args:
            text: Text to count tokens

        Returns:
            Token count
        """
        return len(self.tokenizer.encode(text))

    def chunk_text(self, text: str) -> List[str]:
        """
        Chunk text into overlapping segments

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        if not text or not text.strip():
            return []

        # Split into paragraphs first (preserve natural boundaries)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = self.count_tokens(para)

            # If single paragraph exceeds chunk size, split it
            if para_size > self.config.chunk_size:
                # Add current chunk if not empty
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = []
                    current_size = 0

                # Split large paragraph
                para_chunks = self._split_large_text(para)
                chunks.extend(para_chunks)
                continue

            # Check if adding paragraph would exceed chunk size
            if current_size + para_size > self.config.chunk_size and current_chunk:
                # Save current chunk
                chunks.append('\n\n'.join(current_chunk))

                # Start new chunk with overlap
                overlap_size = 0
                overlap_paras = []

                # Add paragraphs from end until we reach overlap size
                for prev_para in reversed(current_chunk):
                    prev_size = self.count_tokens(prev_para)
                    if overlap_size + prev_size <= self.config.chunk_overlap:
                        overlap_paras.insert(0, prev_para)
                        overlap_size += prev_size
                    else:
                        break

                current_chunk = overlap_paras
                current_size = overlap_size

            # Add paragraph to current chunk
            current_chunk.append(para)
            current_size += para_size

        # Add final chunk
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            if self.count_tokens(chunk_text) >= self.config.min_chunk_size:
                chunks.append(chunk_text)

        return chunks

    def _split_large_text(self, text: str) -> List[str]:
        """
        Split large text that exceeds chunk size

        Uses sentence boundaries when possible.

        Args:
            text: Text to split

        Returns:
            List of chunks
        """
        # Try splitting by sentences
        sentences = self._split_sentences(text)

        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = self.count_tokens(sentence)

            # If single sentence exceeds chunk size, split by words
            if sentence_size > self.config.chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_size = 0

                word_chunks = self._split_by_words(sentence)
                chunks.extend(word_chunks)
                continue

            # Check if adding sentence would exceed chunk size
            if current_size + sentence_size > self.config.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))

                # Start new chunk with overlap (last few sentences)
                overlap_size = 0
                overlap_sentences = []

                for prev_sent in reversed(current_chunk[-3:]):  # Last 3 sentences for overlap
                    prev_size = self.count_tokens(prev_sent)
                    if overlap_size + prev_size <= self.config.chunk_overlap:
                        overlap_sentences.insert(0, prev_sent)
                        overlap_size += prev_size
                    else:
                        break

                current_chunk = overlap_sentences
                current_size = overlap_size

            current_chunk.append(sentence)
            current_size += sentence_size

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences

        Simple sentence splitter based on punctuation.

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        import re

        # Split on sentence-ending punctuation followed by space and capital letter
        pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(pattern, text)

        return [s.strip() for s in sentences if s.strip()]

    def _split_by_words(self, text: str) -> List[str]:
        """
        Split text by words when sentences are too large

        Args:
            text: Text to split

        Returns:
            List of chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            word_size = self.count_tokens(word + ' ')

            if current_size + word_size > self.config.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))

                # Small overlap (last few words)
                overlap_words = current_chunk[-10:]  # Last 10 words
                current_chunk = overlap_words
                current_size = self.count_tokens(' '.join(overlap_words))

            current_chunk.append(word)
            current_size += word_size

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def chunk_with_metadata(self, text: str, base_metadata: Optional[dict] = None) -> List[dict]:
        """
        Chunk text and return chunks with metadata

        Args:
            text: Text to chunk
            base_metadata: Base metadata to include in all chunks

        Returns:
            List of dicts with 'content' and 'metadata' keys
        """
        chunks = self.chunk_text(text)

        result = []
        for i, chunk in enumerate(chunks):
            metadata = base_metadata.copy() if base_metadata else {}
            metadata.update({
                'chunk_index': i,
                'total_chunks': len(chunks),
                'token_count': self.count_tokens(chunk),
                'char_count': len(chunk)
            })

            result.append({
                'content': chunk,
                'metadata': metadata
            })

        return result


# Global chunker instance (lazy loaded)
_chunker: Optional[DocumentChunker] = None


def get_chunker(reload: bool = False) -> DocumentChunker:
    """
    Get global document chunker (singleton pattern)

    Args:
        reload: Force reload

    Returns:
        DocumentChunker instance
    """
    global _chunker

    if _chunker is None or reload:
        _chunker = DocumentChunker()

    return _chunker


def chunk_text(text: str) -> List[str]:
    """
    Quick helper to chunk text

    Args:
        text: Text to chunk

    Returns:
        List of chunks
    """
    chunker = get_chunker()
    return chunker.chunk_text(text)


if __name__ == "__main__":
    # Test chunker
    print("Testing document chunker...")

    # Sample text
    text = """
    This is a test document with multiple paragraphs.
    It will be split into chunks for testing.

    The second paragraph continues here.
    We want to see how the chunker handles this.

    And here is a third paragraph for good measure.
    The chunker should maintain context through overlap.
    """

    chunker = DocumentChunker()
    chunks = chunker.chunk_text(text)

    print(f"✓ Text split into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        token_count = chunker.count_tokens(chunk)
        print(f"\nChunk {i + 1} ({token_count} tokens):")
        print(chunk[:100] + "..." if len(chunk) > 100 else chunk)