import ollama


def test_embedding():

    example_text = "Political language is designed to make lies sound truthful"

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=example_text
    )

    embedding = response.embedding

    assert (type(embedding) == list)
    assert (len(embedding) > 0)


def test_embedding_classes():

    from src.embedding import OllamaEmbeddingModel

    example_text = "Political language is designed to make lies sound truthful"

    embedder = OllamaEmbeddingModel()

    embedding = embedder.embed_one(example_text)

    assert (type(embedding) == list)
    assert (len(embedding) > 0)

    embeddings = embedder.embed([
        "Political language is designed to make lies sound truthful",
        "In individuals, insanity is rare; but in groups, parties, nations and epochs, it is the rule."
    ])

    assert (type(embeddings) == list)
