from fastapi import FastAPI  # Web framework for API
from pydantic import BaseModel  # For request validation
from huggingface_hub import InferenceClient  # Hugging Face Inference API client
import uvicorn  # ASGI server
import os  # To access environment variables

# Get Hugging Face API token from environment variable
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set!")  # Stop if token is missing

# Initialize the Hugging Face client
client = InferenceClient(
    provider="hf-inference", 
    api_key=HF_TOKEN,
)

# Create FastAPI app
app = FastAPI()

# Home endpoint to verify the API is running
@app.get("/")
def home():
    return {"message": "Sentence Similarity API is running!"}

# Request model for sentence similarity
class Sentences(BaseModel):
    source_sentence: str
    other_sentences: list[str]

# Sentence similarity endpoint
@app.post("/similarity")
async def similarity(data: Sentences):
    try:
        # Call Hugging Face sentence similarity model
        result = client.sentence_similarity(
            data.source_sentence,
            data.other_sentences,
            model="sentence-transformers/all-MiniLM-L6-v2"
            # Alternative model for Farsi: "sentence-transformers/distiluse-base-multilingual-cased-v2"
        )

        # Format the response
        return {"result": [
            {"sentence": s, "similarity": float(score)}
            for s, score in zip(data.other_sentences, result)
        ]}
    except Exception as e:
        # Return any exception as an error message
        return {"error": str(e)}

# Run the API server if executed directly
if __name__ == "__main__":
    print("Starting API server on http://127.0.0.1:8001 ...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
