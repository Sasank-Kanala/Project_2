import pandas as pd

# Hardcoded overrides (highest priority)
HARDCODED_TOPIC_DEPARTMENT_MAP = {
    "Transaction Assistance": "Payments Operations",
    "Security Related": "Fraud & Security",
    "Card Block / Unblock": "Cards Operations",
    "Loan EMI / Auto Debit": "Auto Finance Operations",
    "Card Delivery / Replacement": "Cards Operations",
    "KYC / Verification (Loan-specific)": "Auto Finance Operations",
}


def build_topic_department_map(training_df: pd.DataFrame) -> dict:
    """
    Build Topic → Resolution Department mapping
    Uses majority vote per topic from training data
    """

    training_df["topic"] = training_df["topic"].astype(str).str.strip()
    training_df["resolution_department"] = (
        training_df["resolution_department"].astype(str).str.strip()
    )

    return (
        training_df
        .groupby("topic")["resolution_department"]
        .agg(lambda x: x.value_counts().idxmax())
        .to_dict()
    )


def assign_department(
    predicted_topic: str,
    topic_department_map: dict
) -> str:
    """
    Assign department using:
    1. Hardcoded override
    2. Majority-vote fallback
    """

    if predicted_topic in HARDCODED_TOPIC_DEPARTMENT_MAP:
        return HARDCODED_TOPIC_DEPARTMENT_MAP[predicted_topic]

    return topic_department_map.get(predicted_topic, "Unassigned")
