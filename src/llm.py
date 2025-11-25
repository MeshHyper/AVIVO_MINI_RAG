from langchain_ollama import ChatOllama

from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


model = ChatOllama(model="gemma3:1b-it-qat", temperature=0.2)


prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables = ['context', 'question']
)


def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

def parallel_chain(retriever,format_docs=format_docs):
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })
    return parallel_chain

parser = StrOutputParser()
def main_chain(parallel_chain):
    main_chain = parallel_chain | prompt | model | parser
    return main_chain