from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import json
import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from llm_providers import OpenAIProvider

load_dotenv()
app = FastAPI()
provider = OpenAIProvider()

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(image_file) -> str:
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

@app.post("/triage")
async def triage(message: str = Form(None), file: UploadFile = File(None)):
    if file:
        if file.filename.endswith(".pdf"):
            with open(file.filename, "wb") as f:
                f.write(await file.read())
            message = extract_text_from_pdf(file.filename)
        elif file.filename.endswith((".jpg", ".jpeg", ".png")):
            content = await file.read()
            with open(file.filename, "wb") as f:
                f.write(content)
            message = extract_text_from_image(file.filename)

    if not message:
        return {"error": "No message or supported file provided."}

    result = provider.classify(message)
    return result
