import os
import re

from flask import Flask, jsonify, render_template, request
from textblob import TextBlob

app = Flask(__name__)

MAX_LENGTH = 5000  # safety limit on input size


def preprocess(text):
    """Basic cleaning and tokenization."""
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)  # remove URLs
    text = re.sub(r"\s+", " ", text).strip()            # collapse whitespace
    tokens = re.findall(r"[A-Za-z']+", text)            # simple word tokens
    return text, tokens


def classify(polarity):
    """Map the polarity score to a sentiment label."""
    if polarity > 0:
        return "Positive"
    if polarity < 0:
        return "Negative"
    return "Neutral"


def analyze_text(raw_text):
    """Run the full workflow. Returns (result, error)."""
    text = (raw_text or "").strip()

    if not text:
        return None, "Please enter some text before analyzing."
    if len(text) > MAX_LENGTH:
        return None, f"Text is too long. Please keep it under {MAX_LENGTH} characters."

    cleaned, tokens = preprocess(text)
    if not tokens:
        return None, "Please enter some meaningful words to analyze."

    blob = TextBlob(cleaned)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)

    return {
        "sentiment": classify(polarity),
        "polarity": polarity,
        "subjectivity": subjectivity,
        "word_count": len(tokens),
        "marker": round((polarity + 1) / 2 * 100, 1),  # 0-100% position on the scale
    }, None


@app.route("/", methods=["GET", "POST"])
def index():
    """Page route. The POST branch keeps the form working even without JavaScript."""
    result, error, text = None, None, ""
    if request.method == "POST":
        text = request.form.get("text", "")
        result, error = analyze_text(text)
    return render_template("index.html", text=text, result=result, error=error)


@app.route("/analyze", methods=["POST"])
def analyze():
    """JSON endpoint used by the page's script."""
    data = request.get_json(silent=True) or {}
    result, error = analyze_text(data.get("text", ""))
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
