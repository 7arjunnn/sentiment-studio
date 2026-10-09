# Sentiment Studio

Understand the emotion behind every word. Sentiment Studio is a small web app that reads a piece of text and reports whether its tone is **Positive**, **Negative**, or **Neutral**, along with a polarity score and a subjectivity score.

## Features

- Large text workspace with a character counter
- One-click example sentences
- Result card with sentiment status, polarity, subjectivity, and a polarity indicator
- Loading, empty-input, and error states
- Responsive layout for desktop and mobile
- Works with JavaScript on (instant results) or off (standard form submit)

## Technologies

- Frontend: HTML and CSS (plus a few lines of vanilla JavaScript for the loading state and example buttons)
- Backend: Python, Flask
- NLP: TextBlob
- Production server: Gunicorn

## How it works

1. The text is sent to the Flask backend (`POST /analyze`, or the form on `/`).
2. It is cleaned (URLs removed, whitespace collapsed) and tokenized.
3. TextBlob computes polarity (-1 to +1) and subjectivity (0 to 1).
4. The label is chosen from polarity: above 0 is Positive, below 0 is Negative, exactly 0 is Neutral.
5. The page displays the real values returned by the backend.

## Project structure

```text
sentiment-analysis/
├── app.py              Flask app and analysis logic
├── requirements.txt    Flask, TextBlob, Gunicorn
├── render.yaml         Render deployment settings
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Run locally

```bash
cd sentiment-analysis
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Deploy on Render (free, public HTTPS link)

1. Create a free account at https://github.com and a new **public** repository named `sentiment-studio`.
2. Upload every file in this folder to that repository (the GitHub web page has an "Add file > Upload files" button). Keep `app.py`, `requirements.txt`, `render.yaml`, `templates/` and `static/` at the top level of the repository.
3. Create a free account at https://render.com and choose **Sign in with GitHub**.
4. Click **New +**, then **Web Service**, then pick your `sentiment-studio` repository.
5. If Render does not fill these in from `render.yaml`, enter them manually:
   - Language: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60`
   - Instance type: **Free**
6. Click **Create Web Service** and wait a few minutes for the build.
7. When the status shows **Live**, Render shows your link at the top of the page, in the form `https://sentiment-studio-xxxx.onrender.com`. That is the link to share.

Note: on the free plan the site goes to sleep after a period of inactivity, so the first visit can take around 30 to 60 seconds to wake up. Open the link once yourself shortly before sharing it.

## Example

Input: `I love learning about information retrieval. It is exciting!`
Result: Positive, with a positive polarity and a moderate subjectivity score (computed live by TextBlob).

Input: `The product is amazing but the delivery was horrible.`
Result: the overall sentiment is decided by the combined polarity of the whole sentence.
