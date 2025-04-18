from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import subprocess

app = FastAPI()

# Разрешаем запросы с фронта (в т.ч. Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить конкретными доменами
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), format: str = Form(...)):
    input_ext = file.filename.split(".")[-1]
    input_temp = f"input_{uuid.uuid4()}.{input_ext}"
    output_temp = f"output_{uuid.uuid4()}.{format}"

    # Сохраняем загруженный файл
    with open(input_temp, "wb") as f:
        f.write(await file.read())

    # Преобразуем с помощью ffmpeg
    command = ["ffmpeg", "-i", input_temp, output_temp]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Удаляем входной файл
    os.remove(input_temp)

    # Проверяем успешность
    if os.path.exists(output_temp):
        return FileResponse(output_temp, filename=output_temp)
    else:
        return {"error": "Conversion failed", "details": result.stderr.decode()}
