from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    # Below is the example structure of the expected input data
    # {
    #     "titles": [
    #         "Tesla stocks surged after good earnings report",
    #         "Apple announces new product lineup for 2025",
    #         "Amazon expands into new markets in Asia"
    #     ]
    # }

    titles = data.get("titles", [])

    # Type check: Ensure 'titles' field exists and it is a list
    if not isinstance(titles, list):
        return jsonify({"error": "'titles' must be a list of strings"}), 400
    

    # Resulting variables below
    positive = 0
    negative = 0
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
    app.run(host="0.0.0.0", port=5000, debug=True)
