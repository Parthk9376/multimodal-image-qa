from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import tempfile
from PIL import Image
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    image_base64: str
    question: str

class Response(BaseModel):
    answer: str

@app.post("/answer-image", response_model=Response)
async def answer(req: Request):

    image_bytes = base64.b64decode(req.image_base64)

    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        f.write(image_bytes)
        f.flush()

        img = Image.open(f.name)

        result = model.generate_content(
            [req.question, img]
        )

    return {
        "answer": result.text.strip()
    }
