import mlflow
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# This will create the experiment if it doesn't exist
mlflow.set_experiment("gemma_chatbot")

def log_interaction(user_input: str, model_output: str):
    try:
        with mlflow.start_run():
            mlflow.log_param("user_input", user_input)
            mlflow.log_param("model_output", model_output)
    except Exception as e:
        print(f"MLflow logging failed: {e}")
