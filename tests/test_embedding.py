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
