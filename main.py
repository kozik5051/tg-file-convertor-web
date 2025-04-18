from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или укажи конкретно твою веб-страницу
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/convert")
async def convert_file(file: UploadFile, format: str = Form(...)):
    input_ext = os.path.splitext(file.filename)[1]
    input_path = f"temp/{uuid.uuid4().hex}{input_ext}"
    output_path = f"temp/{uuid.uuid4().hex}.{format if 'pdf' not in format else 'docx' if format == 'pdf_to_word' else 'pdf'}"

    os.makedirs("temp", exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        if format in ["mp3", "wav", "mp4", "avi"]:
            subprocess.run(["ffmpeg", "-i", input_path, output_path], check=True)
        elif format == "pdf_to_word":
            subprocess.run(["libreoffice", "--headless", "--convert-to", "docx", "--outdir", "temp", input_path], check=True)
            output_path = input_path.replace(".pdf", ".docx")
        elif format == "word_to_pdf":
            subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", "temp", input_path], check=True)
            output_path = input_path.replace(".docx", ".pdf")
        else:
            return {"error": "Unknown format"}
    except Exception as e:
        return {"error": str(e)}

    return FileResponse(output_path, filename=os.path.basename(output_path))
