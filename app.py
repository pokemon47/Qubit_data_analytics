import os
from flask import Flask, request, jsonify
from transformers import pipeline # type: ignore

SERVER_ADDRESS = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
PORT = int(os.getenv("FLASK_RUN_PORT", 5000))  # Default to 5000 if not set

app = Flask(__name__)

# Load the sentiment analysis model
model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.route("/", methods=["GET"])
def status():
    return jsonify({"status": "Server is running", "port": PORT}), 200

@app.route("/predict", methods=["POST"])
def predict():
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

if __name__ == "__main__":
    print(f"Starting Flask server at {SERVER_ADDRESS}:{PORT}...")
    app.run(host=SERVER_ADDRESS, port=PORT, debug=False)
