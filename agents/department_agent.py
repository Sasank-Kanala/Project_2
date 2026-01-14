
def assign_department(topic: str):
    mapping = {
        "Loan Closure": "Loans",
        "Account Issue": "Accounts",
        "Card Issue": "Cards"
    }
    return mapping.get(topic, "Customer Support")
