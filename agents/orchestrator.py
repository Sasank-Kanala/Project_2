from agents.topic_agent import detect_topic
from agents.department_agent import assign_department
from agents.llm_agent import generate_response


def process_message(message: str):
    topic, confidence = detect_topic(message)
    department = assign_department(topic)
    resolution = generate_response(message)

    return {
        "topic": topic,
        "department": department,
        "confidence_score": confidence,
        "resolution": resolution
    }
