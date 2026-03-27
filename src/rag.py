from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


def load_vectorstore(persist_directory: str = "./data/chroma") -> Chroma:
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=persist_directory, embedding_function=embeddings
    )


def make_rag_qa(vectorstore: Chroma, model_name: str = "gpt-3.5-turbo"):
    llm = ChatOpenAI(model=model_name, temperature=0.0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Simple RetrievalQA chain. We use 'stuff' chain to include retrieved
    # documents directly.
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    return qa
