from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import List


class EmbeddingModel(ABC):

    @abstractmethod
    def embed(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        pass

    def embed_all(self, texts: List[str]) -> Generator[List[float], None, None]:
        for each_text in texts:
            yield self.embed([each_text])


class OllamaEmbeddingModel(EmbeddingModel):

    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        import ollama

        response = ollama.embeddings(
            model=self.model,
            prompt=texts
        )

        return response.embedding
