# cancer_chat_bot
## 1. Clone the Repository

git clone https://github.com/your-username/cancer-chatbot.git
cd cancer-chat_bot

## 2. Install Dependencies

pip install -r requirements.txt

## 3. Add API Keys in .env
Create a .env file:

GROQ_API_KEY=your_groq_api_key

SERP_API_KEY=your_serpapi_key

## Run the App

python main.py
Then open http://localhost:5000
API Call (POST /chat)
Input:

json

{
  "message": "What are the early symptoms of liver cancer?"
}