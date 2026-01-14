# # import pandas as pd

# # # Hardcoded overrides (highest priority)
# # HARDCODED_TOPIC_DEPARTMENT_MAP = {
# #     "Transaction Assistance": "Payments Operations",
# #     "Security Related": "Fraud & Security",
# #     "Card Block / Unblock": "Cards Operations",
# #     "Loan EMI / Auto Debit": "Auto Finance Operations",
# #     "Card Delivery / Replacement": "Cards Operations",
# #     "KYC / Verification (Loan-specific)": "Auto Finance Operations",
# # }


# # def build_topic_department_map(training_df: pd.DataFrame) -> dict:
# #     """
# #     Build Topic → Resolution Department mapping
# #     Uses majority vote per topic from training data
# #     """

# #     training_df["topic"] = training_df["topic"].astype(str).str.strip()
# #     training_df["resolution_department"] = (
# #         training_df["resolution_department"].astype(str).str.strip()
# #     )

# #     return (
# #         training_df
# #         .groupby("topic")["resolution_department"]
# #         .agg(lambda x: x.value_counts().idxmax())
# #         .to_dict()
# #     )


# # def assign_department(
# #     predicted_topic: str,
# #     topic_department_map: dict
# # ) -> str:
# #     """
# #     Assign department using:
# #     1. Hardcoded override
# #     2. Majority-vote fallback
# #     """

# #     if predicted_topic in HARDCODED_TOPIC_DEPARTMENT_MAP:
# #         return HARDCODED_TOPIC_DEPARTMENT_MAP[predicted_topic]

# #     return topic_department_map.get(predicted_topic, "Unassigned")



# # department_mapper.py

# # Fully hardcoded Topic → Department mapping
# TOPIC_DEPARTMENT_MAP = {
#     "Information": "Customer Support",
#     "Complaints": "Customer Support",
#     "Disputes": "Fraud & Security",
#     "Transaction Assistance": "Payments Operations",
#     "Security Related": "Fraud & Security",
#     "Account Opening": "Accounts Operations",
#     "Account Closing/Modification": "Accounts Operations",
#     "New Products": "Customer Support",
#     "Card Block / Unblock": "Cards Operations",
#     "Card Delivery / Replacement": "Cards Operations",
#     "Loan EMI / Auto Debit": "Auto Finance Operations",
#     "KYC / Verification (Loan)": "Auto Finance Operations",
#     "ATM Issues": "ATM Operations",
#     "Card Issues": "Cards Operations",
#     "Loan Related": "Auto Finance Operations",
#     "Fraud Reports": "Fraud & Security",
# }


# def assign_department(predicted_topic: str) -> str:
#     """
#     Assign department strictly based on predefined Topic → Department rules
#     """

#     predicted_topic = str(predicted_topic).strip()

#     return TOPIC_DEPARTMENT_MAP.get(predicted_topic, "Unassigned")




from agents.customer_support_agent import handle_message as customer_support_agent
from agents.payments_operations_agent import handle_message as payments_agent
from agents.fraud_security_agent import handle_message as fraud_agent
from agents.cards_operations_agent import handle_message as cards_agent
from agents.accounts_operations_agent import handle_message as accounts_agent
from agents.atm_operations_agent import handle_message as atm_agent
from agents.auto_finance_agent import handle_message as auto_finance_agent


TOPIC_DEPARTMENT_MAP = {
    "Information": "Customer Support",
    "Complaints": "Customer Support",
    "Disputes": "Fraud & Security",
    "Transaction Assistance": "Payments Operations",
    "Security Related": "Fraud & Security",
    "Account Opening": "Accounts Operations",
    "Account Closing/Modification": "Accounts Operations",
    "New Products": "Customer Support",
    "Card Block / Unblock": "Cards Operations",
    "Card Delivery / Replacement": "Cards Operations",
    "Loan EMI / Auto Debit": "Auto Finance Operations",
    "KYC / Verification (Loan)": "Auto Finance Operations",
    "ATM Issues": "ATM Operations",
    "Card Issues": "Cards Operations",
    "Loan Related": "Auto Finance Operations",
    "Fraud Reports": "Fraud & Security"
}


DEPARTMENT_AGENT_MAP = {
    "Customer Support": customer_support_agent,
    "Payments Operations": payments_agent,
    "Fraud & Security": fraud_agent,
    "Cards Operations": cards_agent,
    "Accounts Operations": accounts_agent,
    "ATM Operations": atm_agent,
    "Auto Finance Operations": auto_finance_agent
}


def assign_department_and_agent(predicted_topic: str, message: str) -> dict:
    department = TOPIC_DEPARTMENT_MAP.get(predicted_topic, "Customer Support")

    agent_func = DEPARTMENT_AGENT_MAP.get(department)

    if agent_func:
        agent_response = agent_func(message)
    else:
        agent_response = {
            "agent_name": "Unknown Agent",
            "agent_status": "Not Assigned",
            "agent_output": "No agent available for this department."
        }

    return {
        "predicted_resolution_department": department,
        "agent_response": agent_response
    }
