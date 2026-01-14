def generate_resolution(topic: str) -> str:
    responses = {
        "Loan": "Our loan team will assist you shortly.",
        "Refund": "Your refund is being reviewed.",
        "Account": "We are checking your account details.",
        "General": "Our support team will get back to you."
    }

    return responses.get(topic, "Support will assist you.")
