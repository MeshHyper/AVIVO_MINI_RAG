from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma
import warnings

import os
warnings.filterwarnings("ignore", category=DeprecationWarning)
embedding = HuggingFaceEmbeddings(model_name='Qwen/Qwen3-Embedding-0.6B')

def document_loader(path):
    loader = DirectoryLoader(
    path=path,
    glob='*.md',
    loader_cls=UnstructuredMarkdownLoader,
    loader_kwargs={'mode': 'single'}
)
    
    return loader


splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=300,
    chunk_overlap=0,
)

def chunking(docs, splitter=splitter):
    all_chunks = []

    for doc in docs:
        pieces = splitter.create_documents([doc.page_content])
        all_chunks.extend(pieces)
    return all_chunks


def create_vector_store(all_chunks, embedding=embedding):
    persist_dir = "my_chroma_db"

    if os.path.exists(persist_dir):
        vector_store = Chroma(
            persist_directory=persist_dir,
            collection_name='sample',
            embedding_function=embedding
        )
    else:
        vector_store = Chroma(
            persist_directory=persist_dir,
            collection_name='sample',
            embedding_function=embedding
        )

    vector_store.add_documents(all_chunks)
    vector_store.persist()

    return vector_store






