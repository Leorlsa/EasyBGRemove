import logging
from flask import Flask, render_template, request, jsonify
from rembg import remove
from PIL import Image
import base64
from io import BytesIO


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return 'Nenhuma imagem encontrada'

    image = request.files['image']
    if image.filename == '':
        return 'Nome do arquivo não encontrado'

    try:
        img = Image.open(image)
        img = img.convert("RGBA")  # Converter para o formato RGBA
        img_without_back = remove(img)
        output_buffer = BytesIO()
        img_without_back.save(output_buffer, format='PNG')
        output_buffer.seek(0)

        image_data = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        logging.info("Imagem processada com sucesso")
    except Exception as e:
        logging.error("Erro ao processar a imagem: %s", str(e))
        return 'Erro ao processar a imagem'

    return render_template('result.html', image_data=image_data, show_enhancement_option=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
