from agents.customer_support_agent import handle_message as customer_support
from agents.fraud_security_agent import handle_message as fraud_security
from agents.cards_operations_agent import handle_message as cards_ops
from agents.payments_operations_agent import handle_message as payments_ops
from agents.accounts_operations_agent import handle_message as accounts_ops
from agents.auto_finance_agent import handle_message as auto_finance
from agents.atm_operations_agent import handle_message as atm_ops

def route_to_agent(department: str, message: str):
    if department == "Customer Support":
        return customer_support(message)
    elif department == "Fraud & Security":
        return fraud_security(message)
    elif department == "Cards Operations":
        return cards_ops(message)
    elif department == "Payments Operations":
        return payments_ops(message)
    elif department == "Accounts Operations":
        return accounts_ops(message)
    elif department == "Auto Finance Operations":
        return auto_finance(message)
    elif department == "ATM Operations":
        return atm_ops(message)
    else:
        return {
            "agent": "Unknown",
            "response": "Your request has been forwarded for manual review."
        }
