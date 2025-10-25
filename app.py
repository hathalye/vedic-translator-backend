from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.file_handler import extract_text_from_file, create_docx_from_text
from utils.translator import translate_text
import os
import tempfile

app = Flask(__name__)
CORS(app)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "gist")  # "transliterate", "literal", "gist"

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        translated_text = translate_text(text, mode=mode)
        return jsonify({"translated_text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        text = extract_text_from_file(file)
        return jsonify({"extracted_text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download", methods=["POST"])
def download_file():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        temp_file_path = create_docx_from_text(text)
        return send_file(temp_file_path, as_attachment=True, download_name="translated.docx")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
