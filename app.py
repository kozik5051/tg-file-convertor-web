import os
import tempfile
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import subprocess
from pdf2docx import Converter
from docx2pdf import convert as docx_to_pdf

app = Flask(__name__)

@app.route("/api/convert", methods=["POST"])
def convert_file():
    if "file" not in request.files or "format" not in request.form:
        return "Missing file or format", 400

    uploaded_file = request.files["file"]
    target_format = request.form["format"]

    filename = secure_filename(uploaded_file.filename)
    input_path = os.path.join(tempfile.gettempdir(), filename)
    uploaded_file.save(input_path)

    base, ext = os.path.splitext(input_path)
    output_path = ""

    try:
        if target_format == "pdf_to_word":
            output_path = f"{base}.docx"
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()

        elif target_format == "word_to_pdf":
            output_path = f"{base}.pdf"
            docx_to_pdf(input_path, output_path)

        elif target_format in ["mp3", "wav", "mp4", "avi"]:
            output_path = f"{base}_converted.{target_format}"
            cmd = ["ffmpeg", "-i", input_path, output_path]
            subprocess.run(cmd, check=True)

        else:
            return "Unknown format", 400

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("Conversion error:", e)
        return "Conversion failed", 500

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
