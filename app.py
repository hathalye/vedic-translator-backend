from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import requests
from utils.file_handler import extract_text_from_file, create_docx_from_text
from utils.translator import transliterate_text, translate_literal, translate_gist

app = Flask(__name__)
CORS(app)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    mode = data.get('mode', 'gist')
    target_lang = data.get('target_lang', 'en')

    if not text.strip():
        return jsonify({'error': 'Empty input'}), 400

    if mode == 'transliterate':
        output = transliterate_text(text)
    elif mode == 'literal':
        output = translate_literal(text, target_lang)
    else:
        output = translate_gist(text, target_lang)

    return jsonify({'output': output})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    text, warning = extract_text_from_file(file)
    return jsonify({'text': text, 'warning': warning})

@app.route('/download', methods=['POST'])
def download_docx():
    data = request.get_json()
    translated_text = data.get('text', '')
    docx_bytes = create_docx_from_text(translated_text)

    return send_file(
        io.BytesIO(docx_bytes),
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='translated_output.docx'
    )

@app.route('/')
def home():
    return "Vedic Translator Backend Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
