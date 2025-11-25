from src.indexing import document_loader,chunking,create_vector_store
from src.llm import parallel_chain,main_chain

def generator(question):
    loader = document_loader(path = 'data')

    docs = loader.load()
    all_chunks = chunking(docs=docs)


    vector_store = create_vector_store(all_chunks=all_chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    parallel_chains = parallel_chain(retriever=retriever)
    parallel = main_chain(parallel_chain=parallel_chains)


    response = parallel.invoke(question)
    return response

if __name__ == "__main__":
    print(generator("Why my password is not working?"))


