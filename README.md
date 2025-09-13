## Gemma Chatbot 

A chatbot using Gemma-3-27B-IT, FastAPI backend, MLflow logging, and a modern frontend.

## Project Overview

Backend: FastAPI + Python

Model: Gemma-3-27B-IT running locally on port 8018

Frontend: HTML, CSS, JS

Logging & Monitoring: MLflow

Goal: Chat with Gemma, track interactions, and view analytics via MLflow UI

## 1️⃣ Clone the Project
```git clone https://github.com/yourusername/gemma-chatbot.git
cd gemma-chatbot
```

## 2️⃣ Set Up Python Environment
```python3 -m venv gemmaenv
source gemmaenv/bin/activate   # Linux/macOS
pip install --upgrade pip
```

## 3️⃣ Install Backend Dependencies
``` cd backend
pip install -r requirements.txt
```

## 4️⃣ Deploy Gemma-3-27B-IT Model
Option 1: Using vLLM with Docker (Recommended for GPU isolation)

# Start a screen session
```  screen -S Gemma-3-27B-IT
```
# Navigate to models directory
``` cd models
 git clone https://huggingface.co/google/gemma-3-27b-it
```

# Run Docker container with NVIDIA Triton & vLLM
inside models folder run : 
``` sudo docker run -it --rm --gpus '"device=0,1,2,3"' --shm-size=20g \
  --network host \
  -v "$(pwd)":/workspace --workdir /workspace \
  nvcr.io/nvidia/tritonserver:25.06-vllm-python-py3
```

# Inside container:
``` python3 -m vllm.entrypoints.openai.api_server \
  --model gemma-3-27b-it \
  --port 8018 \
  --enable-auto-tool-choice \
  --tool-call-parser llama3_json \
  --tensor-parallel-size 4 \
  --max-model-len 40000
```

# Test Gemma:
```
curl http://localhost:8018/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{"model": "gemma-3-27b-it", "messages": [{"role": "user", "content": "hi"}]}'
```

Option 2: Without Docker (Direct Python Execution)
# Activate Python environment
```  source ~/gemmaenv/bin/activate
```
# Navigate to model folder
```  cd models
```
# Run vLLM server directly
``` python3 -m vllm.entrypoints.openai.api_server \
  --model gemma-3-27b-it \
  --port 8018 \
  --enable-auto-tool-choice \
  --tool-call-parser llama3_json \
  --tensor-parallel-size 4 \
  --max-model-len 40000
```

This will launch the API server directly, accessible at http://localhost:8018.

## 5️⃣ Start MLflow Server
```  mkdir -p ~/mlflow/artifacts
```
``` mlflow server \
    --backend-store-uri sqlite:///~/mlflow/mlflow.db \
    --default-artifact-root ~/mlflow/artifacts \
    --host 0.0.0.0 \
    --port 5000
```

URL: http://localhost:5000

## 6️⃣ Start Backend FastAPI
```  cd backend/app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Test API:
```
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message": "hi"}'
```

## 7️⃣ Serve Frontend
``` cd frontend
python3 -m http.server 8080
```

URL: http://localhost:8080
