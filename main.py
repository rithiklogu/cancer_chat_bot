import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from services.query_extractor import validate_cancer_query
from services.web_search import search_web
from services.output_formate import make_json_with_links

load_dotenv()
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"message": " Cancer Assistant API is running!"}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return {"error": "Message is required."}, 400

    validated = validate_cancer_query(user_input)
    if "sorry" in validated.lower():
        return jsonify({"response": validated})

    top_result = search_web(validated)
    if "error" in top_result:
        return jsonify({"response": "No results found."})
    formatted = make_json_with_links(top_result)
    return jsonify({"response": formatted})

if __name__ == "__main__":
    app.run(debug=True)
