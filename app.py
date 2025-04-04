import os
from flask import Flask, request, jsonify
import requests
from transformers import pipeline  # type: ignore

SERVER_ADDRESS = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
PORT = int(os.getenv("FLASK_RUN_PORT", 5000))  # Default to 5000 if not set

app = Flask(__name__)

# Load the sentiment analysis model
model = pipeline("sentiment-analysis",
                 model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to authenticate:


def auth_api_key(api_key):
    auth_url = 'http://170.64.139.10:8080/validate'
    data = {
        'apiKey': api_key
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(auth_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return Exception(f"API key validation failed {response.status_code}")


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Server is running", "port": PORT}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        api_key = request.get_json().get('api_key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 400

        data = request.json
        titles = data.get("titles", [])

        # Type check: Ensure 'titles' field exists and it is a list
        if not isinstance(titles, list):
            return jsonify({"error": "'titles' must be a list of strings"}), 400

        # Initialize counters for positive and negative sentiment
        positive_count = 0
        negative_count = 0
        total = 0
        results = []

        for title in titles:
            result = model(title)
            total += 1
            sentiment = result[0]["label"]

            if sentiment == "POSITIVE":
                positive_count += result[0]["score"]
            elif sentiment == "NEGATIVE":
                negative_count += result[0]["score"]

            results.append({
                "title": title,
                "sentiment": sentiment,
                "score": result[0]["score"]
            })

        return jsonify({
            "total": total,
            "total_positive": positive_count,
            "total_negative": negative_count,
            "results": results,
        })
    except Exception as e:
        error_msg = str(e)
        status_code = 401 if "API key validation failed" in error_msg else 403
        return jsonify({"error": error_msg}), status_code


if __name__ == "__main__":
    print(f"Starting Flask server at {SERVER_ADDRESS}:{PORT}...")
    app.run(host=SERVER_ADDRESS, port=PORT, debug=False)
