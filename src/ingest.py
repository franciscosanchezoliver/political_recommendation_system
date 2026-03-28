from typing import List
import logging


from pypdf import PdfReader


from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma

logger = logging.getLogger(__name__)


def _transform_pdf_to_text(pdf_file_path) -> str:
    pdf_reader = PdfReader(pdf_file_path)
    text = ""

    for index, each_page in enumerate(pdf_reader.pages):
        logger.info("Page [%s]: parsing from PDF page to text", index)
        text += f"---- START PAGE {index} ----"
        text += each_page.extract_text() + "\n"
        text += f"---- END PAGE {index} ----"

    return {
        "text": text
    }


def pdf_to_text_paths(pdf_paths: List[str]) -> List[str]:
    texts = []
    for p in pdf_paths:
        loader = PyPDFLoader(p)
        docs = loader.load()
        page_texts = [d.page_content for d in docs]
        texts.append("\n\n".join(page_texts))
    return texts


def chunk_texts(texts: List[str], chunk_size=1000, chunk_overlap=200):

    logging.info(
        f"Chunking texts, "
        f"chunk_size: [{chunk_size}], "
        f"chunk_overlap: [{chunk_overlap}], "
    )

    # Divide texts into chunks for better embedding.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    text_chunks = []
    for t in texts:
        text_chunks.extend(splitter.split_text(t))

    logging.info(f"Chunking complete. Generated {len(text_chunks)} chunks.")

    return text_chunks


def create_or_update_vectorstore(
    texts: List[str], persist_directory: str = "./data/chroma"
):
    # Use OpenAI embeddings by default (requires OPENAI_API_KEY). Fallback to
    # sentence-transformers if OpenAI isn't available.
    try:
        embeddings = OpenAIEmbeddings()
    except Exception:
        # lazy fallback
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")

        class STEmbeds:
            def __call__(self, texts):
                return model.encode(texts).tolist()

        embeddings = STEmbeds()

    vectordb = Chroma.from_texts(
        texts, embeddings, persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb


def ingest_pdfs(
    pdf_paths: List[str], persist_directory: str = "./data/chroma"
):
    texts = []
    for each_pdf in pdf_paths:
        logger.info("Ingesting PDF: %s", each_pdf)

        # Read the PDF and extract text
        pdf_text = _transform_pdf_to_text(each_pdf)
        texts.append(pdf_text["text"])

    chunks = chunk_texts(texts)
    return create_or_update_vectorstore(
        chunks, persist_directory=persist_directory
    )
