import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

llm = ChatGroq(model_name="llama3-8b-8192", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "You are a medical assistant. Format the given search result into a JSON with these keys:\n"
    "- Symptoms\n"
    "- Treatment\n"
    "- Diagnosis\n"
    "- FAQ\n"
    "- Other\n\n"
    "Each value should be a list of strings.\n"
    "Include the source link in the strings if useful.\n"
    "⚠️ DO NOT generate any extra information.\n"
    "Return ONLY valid JSON. Skip empty keys (do not return keys with empty lists).\n\n"
    "{context}"
)

chain = create_stuff_documents_chain(llm, prompt)

def make_json_with_links(result: dict) -> dict:
    try:
        text = f"Title: {result['title']}\nSnippet: {result['snippet']}\nLink: {result['link']}"
        docs = [Document(page_content=text)]
        raw = chain.invoke({"context": docs})

        start = raw.find("{")
        end = raw.rfind("}") + 1
        parsed = json.loads(raw[start:end])

        return {k: v for k, v in parsed.items() if isinstance(v, list) and v}
    except Exception as e:
        return {"error": "Failed to format JSON", "details": str(e)}
