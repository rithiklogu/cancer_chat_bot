import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def validate_cancer_query(user_input: str) -> str:
    prompt = (
        "You are a strict medical classifier.\n"
        "Check if the user's message is clearly related to cancer (like symptoms, treatment, diagnosis, prevention, types, etc).\n"
        "Respond with exactly:\n"
        "  - cancer → if it is clearly about cancer\n"
        "  - not_cancer → if it is unrelated to cancer\n\n"
        f"User: {user_input}\n\n"
        "Answer (only 'cancer' or 'not_cancer'):"
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip().lower()
    return user_input if result == "cancer" else "Sorry, I can only help with cancer-related medical questions."
