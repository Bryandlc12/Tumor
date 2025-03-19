from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Ruta de la carpeta donde se almacenarán las imágenes
UPLOAD_FOLDER = 'static/imagenes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegúrate de que la carpeta existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Lista de imágenes fijas y sus títulos
images_with_titles = [
    {"filename": "ImagenOriginal.jpeg", "title": "MRI del Cerebro"},
    {"filename": "Imagen2.jpeg", "title": "Máscara"},
    {"filename": "Imagen1.jpeg", "title": "MRI con Máscara"}
]

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Si el formulario envía una imagen
        if 'file' not in request.files:
            return 'No hay archivo en la solicitud'
        file = request.files['file']
        if file.filename == '':
            return 'No seleccionaste ninguna imagen'

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)  # Guardar la imagen subida en la carpeta
            return redirect(url_for('index'))  # Recargar la página después de subir

    # Renderizamos las imágenes con sus títulos después de subir
    return render_template('index.html', images_with_titles=images_with_titles)

# Ruta para servir imágenes subidas
@app.route('/imagenes/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
