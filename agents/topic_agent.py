
def detect_topic(message: str) -> str:
    message = message.lower()

    if "loan" in message:
        return "Loan"
    elif "card" in message:
        return "Card"
    elif "account" in message:
        return "Account"
    else:
        return "General"


# import re
# import joblib
# import os

# # ===============================
# # LOAD MODEL & VECTORIZER
# # ===============================
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "models", "topic_lr_model.joblib")
# VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "topic_vectorizer.joblib")

# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECTORIZER_PATH)


# # ===============================
# # TEXT CLEANING (SAME AS YOUR CODE)
# # ===============================
# def clean_text(text: str) -> str:
#     text = str(text).lower()
#     text = re.sub(r"[^a-z0-9 ]", " ", text)
#     text = re.sub(r"\s+", " ", text).strip()
#     return text


# # ===============================
# # TOPIC DETECTION (LR)
# # ===============================
# def detect_topic(message: str):
#     cleaned = clean_text(message)
#     X_vec = vectorizer.transform([cleaned])

#     predicted_topic = model.predict(X_vec)[0]
#     confidence = float(model.predict_proba(X_vec).max())

#     return predicted_topic, confidence
