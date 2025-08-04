import random
from transformers import pipeline

# Load emotion-classification pipeline
emotion_pipeline = pipeline(
    "text-classification",
    model="nateraw/bert-base-uncased-emotion",
    return_all_scores=True
)

CRISIS_KEYWORDS = [
    "suicidal", "kill myself", "end my life",
    "want to die", "hurt myself"
]

# Detect dominant emotion and its confidence score
def detect_emotion(text: str):
    results = emotion_pipeline(text)[0]
    top = max(results, key=lambda x: x["score"])
    return top["label"].lower(), float(top["score"])

# Simple crisis detection by keyword
def is_crisis(text: str):
    t = text.lower()
    return any(k in t for k in CRISIS_KEYWORDS)

# Generate CBT-style empathetic responses per emotion
def generate_response(emotion: str):
    templates = {
        "sadness": [
            "I'm really sorry you're feeling down. Would you like to share more about what's on your mind?",
            "I hear that things feel heavy right now. What’s been the hardest part?"
        ],
        "joy": [
            "That's wonderful to hear! What’s been making you feel happy today?",
            "It’s great you’re feeling good. Tell me more about what’s bringing you joy."
        ],
        "anger": [
            "It sounds like you're upset. What do you think triggered this feeling?",
            "Anger can be tough. Would talking about what’s frustrating you help?"
        ],
        "fear": [
            "It seems like you’re feeling anxious. What’s worrying you the most?",
            "Anxiety can be overwhelming. Do you want to describe what’s on your mind?"
        ],
        "surprise": [
            "That sounds unexpected. How are you processing this surprise?",
            "Surprises can be unsettling. Would you like to explore how you feel about it?"
        ],
        "neutral": [
            "Thank you for sharing. How else have you been feeling lately?",
            "I'm here to listen whenever you want to talk more."
        ]
    }
    return random.choice(templates.get(emotion, templates["neutral"]))
  
