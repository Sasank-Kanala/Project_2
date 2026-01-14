from fastapi import APIRouter, UploadFile, File
import pandas as pd

from knowledge.excel_loader import (
    load_training_data,
    label_messages,
    safe_float
)

router = APIRouter()


@router.post("/upload-test-file")
def upload_test_file(file: UploadFile = File(...)):

    # Load training data
    # train_df = load_training_data("knowledge/Training_Book1.xlsx")
    train_df = load_training_data("knowledge\Training_Book1_2.xlsx")

    # Load test data
    test_df = pd.read_excel(file.file)

    # Normalize column names
    test_df.columns = (
        test_df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    required_cols = {"message", "topic", "resolution_department"}
    missing = required_cols - set(test_df.columns)

    if missing:
        return {"error": f"Uploaded file missing columns: {missing}"}

    test_df["message"] = test_df["message"].astype(str).str.lower().str.strip()
    test_df["actual_topic"] = test_df["topic"].astype(str).str.strip()
    test_df["actual_resolution_department"] = (
        test_df["resolution_department"].astype(str).str.strip()
    )

    # Predict
    result_df = label_messages(train_df, test_df)

    # Accuracy
    result_df["topic_correct"] = (
        result_df["predicted_topic"] == result_df["actual_topic"]
    )

    result_df["department_correct"] = (
        result_df["predicted_resolution_department"]
        == result_df["actual_resolution_department"]
    )

    topic_accuracy = safe_float(result_df["topic_correct"].mean())
    department_accuracy = safe_float(result_df["department_correct"].mean())

    incorrect_topic_count = int((~result_df["topic_correct"]).sum())
    incorrect_department_count = int((~result_df["department_correct"]).sum())

    result_df = result_df.fillna("")

    return {
        "total_records": len(result_df),
        "topic_accuracy": topic_accuracy,
        "department_accuracy": department_accuracy,
        "incorrect_topic_predictions": incorrect_topic_count,
        "incorrect_department_predictions": incorrect_department_count,
        "results": result_df.to_dict(orient="records")
    }


