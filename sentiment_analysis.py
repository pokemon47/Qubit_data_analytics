from flask import Flask, request, jsonify
from transformers import pipeline

# Define constants for the server address and port
SERVER_ADDRESS = "127.0.0.1"
PORT = 5000

app = Flask(__name__)

# Load the sentiment analysis model
model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

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
