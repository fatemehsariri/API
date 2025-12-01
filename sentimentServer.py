from huggingface_hub import InferenceClient  # For Hugging Face Inference API
from fastapi import FastAPI  # Web framework for API
from pydantic import BaseModel  # For request data validation
import uvicorn  # ASGI server
import os  # To access environment variables

# Get Hugging Face API token from environment variable
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set!")  # Error if token is missing

# Initialize Hugging Face Inference client
client = InferenceClient(
    provider="hf-inference", 
    api_key=HF_TOKEN,
)

# Create FastAPI app
app = FastAPI()

# Map Hugging Face labels to human-readable labels
LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

# Request model for incoming text
class TextRequest(BaseModel):
    text: str

# Sentiment analysis endpoint
@app.post("/sentiment")
def sentiment(data: TextRequest):
    # Get predictions from Hugging Face model
    output = client.text_classification(
        data.text, 
        model="cardiffnlp/twitter-roberta-base-sentiment"
    )
    # Format results with label and score
    result = [{"label": LABEL_MAP[o.label], "score": float(o.score)} for o in output]
    return {"sentiment": result}

# Run the API server when executing this file directly
if __name__ == "__main__":
    print("Starting API server on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
