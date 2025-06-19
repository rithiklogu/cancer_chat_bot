# import os
# import json
# import uuid
# from datetime import datetime
# from flask import Flask, request, jsonify
# from dotenv import load_dotenv

# from services.query_extractor import validate_cancer_query
# from services.web_search import search_web_tool
# from services.output_format import format_result_tool

# load_dotenv()

# app = Flask(__name__)
# os.makedirs("chat_memory", exist_ok=True)

# @app.route("/", methods=["GET"])
# def home():
#     return {"message": "🧠 Cancer Assistant is running with Flask!"}

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     user_input = data.get("message")

#     if not user_input:
#         return jsonify({"error": "Message is required."}), 400

#     query = validate_cancer_query.invoke(user_input)

#     if "sorry" in query.lower():
#         log = {
#             "timestamp": datetime.now().isoformat(),
#             "user_input": user_input,
#             "response": query
#         }
#     else:
#         result = search_web_tool.invoke(query)
#         formatted = format_result_tool.invoke(json.dumps(result))
#         log = {
#             "timestamp": datetime.now().isoformat(),
#             "user_input": user_input,
#             "validated_query": query,
#             "search_result": result,
#             "formatted_output": formatted
#         }

#     # Save log to file
#     file_path = f"chat_memory/{uuid.uuid4().hex}.json"
#     with open(file_path, "w") as f:
#         json.dump(log, f, indent=2)

#     return jsonify(log)

# @app.route("/logs", methods=["GET"])
# def get_logs():
#     files = os.listdir("chat_memory")
#     conversations = []

#     for filename in files:
#         path = os.path.join("chat_memory", filename)
#         with open(path, "r") as f:
#             conversations.append(json.load(f))

#     return jsonify(conversations)

# if __name__ == "__main__":
#     app.run(debug=True)



import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from services.query_extractor import validate_cancer_query
from services.web_search import search_web_tool
from services.output_format import format_result_tool

load_dotenv()
app = Flask(__name__)
os.makedirs("chat_memory", exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return {"message": "🧠 Cancer Assistant is running with Flask!"}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message is required."}), 400

    query = validate_cancer_query.invoke(user_input)

    if "sorry" in query.lower():
        log = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": query
        }

        filename = f"chat_memory/{uuid.uuid4().hex}.json"
        with open(filename, "w") as f:
            json.dump(log, f, indent=2)

        return jsonify({"message": query})

    # Valid cancer query flow
    result = search_web_tool.invoke(query)
    formatted = format_result_tool.invoke(json.dumps(result))

    log = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "validated_query": query,
        "search_result": result,
        "formatted_output": formatted
    }

    filename = f"chat_memory/{uuid.uuid4().hex}.json"
    with open(filename, "w") as f:
        json.dump(log, f, indent=2)

    return jsonify({
        "User_input": user_input,
        # "Responces": formatted,
        "search_result": result,
    })

@app.route("/logs", methods=["GET"])
def get_logs():
    files = os.listdir("chat_memory")
    conversations = []

    for filename in files:
        with open(os.path.join("chat_memory", filename), "r") as f:
            conversations.append(json.load(f))

    return jsonify(conversations)

if __name__ == "__main__":
    app.run(debug=True)
