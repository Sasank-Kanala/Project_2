# # import pandas as pd
# # import numpy as np
# # import torch
# # from sentence_transformers import SentenceTransformer, util


# # from knowledge.department_mapper import (
# #     build_topic_department_map,
# #     assign_department
# # )



# # # Load model once
# # model = SentenceTransformer("all-MiniLM-L6-v2")


# # def safe_float(val):
# #     if val is None or pd.isna(val) or np.isinf(val):
# #         return 0.0
# #     return float(val)


# # def load_training_data(path: str) -> pd.DataFrame:
# #     df = pd.read_excel(path)

# #     # Normalize column names
# #     df.columns = (
# #         df.columns
# #         .str.lower()
# #         .str.strip()
# #         .str.replace(" ", "_")
# #     )

# #     required = {"message", "topic", "resolution_department"}
# #     missing = required - set(df.columns)

# #     if missing:
# #         raise ValueError(f"Missing columns in training file: {missing}")

# #     # Clean text
# #     df["message"] = df["message"].astype(str).str.lower().str.strip()
# #     df["topic"] = df["topic"].astype(str).str.strip()
# #     df["resolution_department"] = df["resolution_department"].astype(str).str.strip()

# #     # Encode messages
# #     embeddings = model.encode(
# #         df["message"].tolist(),
# #         convert_to_tensor=True
# #     )

# #     df["embedding"] = list(embeddings)

# #     return df


# # def label_messages(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:

# #     # Build topic → department map from training data
# #     topic_department_map = build_topic_department_map(train_df)

# #     # Stack embeddings
# #     train_embeddings = torch.stack(train_df["embedding"].tolist())

# #     predicted_topics = []
# #     predicted_departments = []
# #     confidence_scores = []

# #     for msg in test_df["message"].tolist():

# #         emb = model.encode(msg, convert_to_tensor=True)

# #         sims = util.cos_sim(emb, train_embeddings)[0]
# #         best_idx = int(torch.argmax(sims))

# #         predicted_topic = train_df.iloc[best_idx]["topic"]

# #         # NEW: department assignment logic
# #         predicted_department = assign_department(
# #             predicted_topic,
# #             topic_department_map
# #         )

# #         predicted_topics.append(predicted_topic)
# #         predicted_departments.append(predicted_department)
# #         confidence_scores.append(safe_float(sims[best_idx].item()))

# #     test_df["predicted_topic"] = predicted_topics
# #     test_df["predicted_resolution_department"] = predicted_departments
# #     test_df["confidence_score"] = confidence_scores

# #     return test_df


# import pandas as pd
# import numpy as np
# import torch
# from sentence_transformers import SentenceTransformer, util
# from knowledge.department_mapper import assign_department

# model = SentenceTransformer("all-MiniLM-L6-v2")


# def safe_float(val):
#     if val is None or pd.isna(val) or np.isinf(val):
#         return 0.0
#     return float(val)


# def load_training_data(path: str) -> pd.DataFrame:
#     df = pd.read_excel(path)

#     df.columns = (
#         df.columns
#         .str.lower()
#         .str.strip()
#         .str.replace(" ", "_")
#     )

#     required = {"message", "topic"}
#     missing = required - set(df.columns)

#     if missing:
#         raise ValueError(f"Missing columns in training file: {missing}")

#     df["message"] = df["message"].astype(str).str.lower().str.strip()
#     df["topic"] = df["topic"].astype(str).str.strip()

#     embeddings = model.encode(
#         df["message"].tolist(),
#         convert_to_tensor=True
#     )

#     df["embedding"] = list(embeddings)

#     return df


# def label_messages(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:

#     train_embeddings = torch.stack(train_df["embedding"].tolist())

#     predicted_topics = []
#     predicted_departments = []
#     confidence_scores = []

#     for msg in test_df["message"].tolist():

#         emb = model.encode(msg, convert_to_tensor=True)
#         sims = util.cos_sim(emb, train_embeddings)[0]
#         best_idx = int(torch.argmax(sims))

#         predicted_topic = train_df.iloc[best_idx]["topic"]
#         predicted_department = assign_department(predicted_topic)

#         predicted_topics.append(predicted_topic)
#         predicted_departments.append(predicted_department)
#         confidence_scores.append(safe_float(sims[best_idx].item()))

#     test_df["predicted_topic"] = predicted_topics
#     test_df["predicted_resolution_department"] = predicted_departments
#     test_df["confidence_score"] = confidence_scores

#     return test_df





import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

from knowledge.department_mapper import assign_department_and_agent


# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def safe_float(val):
    if val is None or pd.isna(val) or np.isinf(val):
        return 0.0
    return float(val)


def load_training_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Normalize column names
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    required = {"message", "topic", "resolution_department"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns in training file: {missing}")

    # Clean text
    df["message"] = df["message"].astype(str).str.lower().str.strip()
    df["topic"] = df["topic"].astype(str).str.strip()
    df["resolution_department"] = df["resolution_department"].astype(str).str.strip()

    # Encode messages
    embeddings = model.encode(
        df["message"].tolist(),
        convert_to_tensor=True
    )

    df["embedding"] = list(embeddings)

    return df


def label_messages(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:

    # Stack embeddings into a single tensor
    train_embeddings = torch.stack(train_df["embedding"].tolist())

    predicted_topics = []
    predicted_departments = []
    confidence_scores = []
    agent_outputs = []

    for msg in test_df["message"].tolist():

        emb = model.encode(msg, convert_to_tensor=True)

        sims = util.cos_sim(emb, train_embeddings)[0]
        best_idx = int(torch.argmax(sims))

        predicted_topic = train_df.iloc[best_idx]["topic"]
        confidence = safe_float(sims[best_idx].item())

        agent_result = assign_department_and_agent(predicted_topic, msg)

        predicted_topics.append(predicted_topic)
        predicted_departments.append(
            agent_result["predicted_resolution_department"]
        )
        confidence_scores.append(confidence)
        agent_outputs.append(agent_result["agent_response"])

    test_df["predicted_topic"] = predicted_topics
    test_df["predicted_resolution_department"] = predicted_departments
    test_df["confidence_score"] = confidence_scores
    test_df["agent_response"] = agent_outputs

    return test_df
