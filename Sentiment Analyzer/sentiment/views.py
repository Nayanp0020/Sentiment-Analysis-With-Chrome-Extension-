import pickle
import re
import numpy as np
from django.shortcuts import render
from .forms import TweetForm
from nltk.sentiment.util import mark_negation
from rest_framework.decorators import api_view
from rest_framework.response import Response

# ----------- Load Model & Vectorizer (Only Once) -----------
with open('sentiment_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)


# ----------- Helper Functions -----------

def clean_tweet(text):
    """Basic text cleaning for sentiment analysis."""
    text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"#\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


def predict_sentiment_label(text):
    """Predict sentiment and confidence for a given text."""
    cleaned = clean_tweet(text)
    tagged = ' '.join(mark_negation(cleaned.split()))
    vec = vectorizer.transform([tagged])

    pred = model.predict(vec)[0]

    # Get probability (if supported)
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(vec)[0]
        confidence = float(np.max(prob))
    else:
        confidence = 1.0  # fallback if model doesn’t support probability

    sentiment = "Positive" if pred == 1 else "Negative"
    return sentiment, confidence


def get_emoji(sentiment):
    """Return emoji for sentiment label."""
    if sentiment == "Positive":
        return "😊"
    elif sentiment == "Negative":
        return "😡"
    else:
        return "😐"


# ----------- Web Page (Form) View -----------

def predict_sentiment(request):
    result = None
    confidence = None
    emoji = None

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.cleaned_data['tweet']
            sentiment, conf = predict_sentiment_label(tweet)
            emoji = get_emoji(sentiment)
            result = sentimen
            confidence = round(conf * 100, 2)
    else:
        form = TweetForm()

    context = {
        'form': form,
        'result': result,
        'confidence': confidence,
        'emoji': emoji
    }
    return render(request, 'predict.html', context)


# ----------- API View for Chrome Extension -----------

@api_view(['POST'])
def analyze_sentiment(request):
    """
    Handles popup sentiment detection for Chrome extension.
    Receives: {"text": "..."}
    Returns: {"sentiment": "Positive", "emoji": "😊", "confidence": 0.87}
    """
    text = request.data.get('text', '').strip()

    if not text:
        return Response({'error': 'No text provided'}, status=400)

    sentiment, confidence = predict_sentiment_label(text)
    emoji = get_emoji(sentiment)

    return Response({
        'sentiment': sentiment,
        'emoji': emoji,
        'confidence': round(confidence * 100, 2)
    })
