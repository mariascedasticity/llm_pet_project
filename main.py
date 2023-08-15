from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Get the API key from the environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Check if the API key is present
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

openai.api_key = openai_api_key

app = FastAPI()

class TextRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/complete-text/")
def complete_text(request: TextRequest):
    prompt = request.prompt
    try:
        response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=150)
        return {"completed_text": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
