import os
from .helpers import LLM
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from .state import GraphState
from langchain.tools import tool


load_dotenv()
groq = os.environ.get("groq")


@tool
def rag_tool(state: GraphState):
    """
    use this tool when there is a pdf involved to answer the question
    """

    def load_pdf(data):
        loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)

        documents = loader.load()

        return documents

    # Create text chunks
    def text_split(extracted_data):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        text_chunks = text_splitter.split_documents(extracted_data)

        return text_chunks

    # download embedding model
    def download_hugging_face_embeddings():
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        return embeddings

    # Load environment variables

    documents = load_pdf("/workspaces/new_rag/data")
    splits = text_split(documents)
    embedding = download_hugging_face_embeddings()
    db = FAISS.from_documents(splits, embedding)

    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer and don't find it in the given context, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        LLM().llm,
        retriever=db.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    result = qa_chain({"query": state["inputs"]})
    answer = result["result"]
    source_documents = [doc.page_content for doc in result["source_documents"]]
    state["answer"] = f"Answer: {answer}\nSource Documents: {source_documents}"

    state["messages"].append("completed rag retrieval")
    return state
