from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# ✅ Add this helper
def enrich_query(user_query: str) -> str:
    base_context = "about SHIVSAR EXPORT company"
    if "shivsar" not in user_query.lower():
        return f"{user_query.strip()} {base_context}"
    return user_query.strip()

def main():
    load_dotenv()
    openai_apikey = os.getenv("OPENAI_API_KEY")

    # 1. Load PDF
    loader = PyPDFLoader("shivsar_export.pdf")
    documents = loader.load()

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    
    # 3. Embed + store in vector DB
    embeddings = OpenAIEmbeddings(openai_api_key=openai_apikey)
    # vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="db")
    # vectordb.persist()

    if os.path.exists("db/chroma.sqlite3"):
        vectordb = Chroma(persist_directory="db", embedding_function=embeddings)
    else:
        vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="db")
        vectordb.persist()

    # 4. LLM setup
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_apikey)

    # 5. Prompt
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an intelligent and friendly assistant for the SHIVSAR EXPORTS ONIONS Company.

Answer all user questions clearly and accurately using only the company information below.

- The user may use broken or short English. Your job is to understand their intent.
- If they mention "contact", "reach", "call", "email", "address", "whatsapp", etc., return actual phone numbers or emails from the data.
- Never guess or fabricate. If not found, say: "Sorry, that information is not available. Visit https://shivsarexport.com for more."

Company Data:
{context}

User Question: {question}
Answer:"""
    )

    # 6. RetrievalQA setup
    retriever = vectordb.as_retriever()
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt}
    )

    user_input = "who is ceo of google"
    enriched = enrich_query(user_input)  # Auto-add company context 
    result = qa.invoke({"query":enriched})

    print("\n Answer:", result)

if __name__ == "__main__":
    main()




