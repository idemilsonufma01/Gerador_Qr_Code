from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
import uuid

app = Flask(__name__)

# Diretório para salvar os QR codes
QR_DIR = os.path.join("static", "qrcodes")
os.makedirs(QR_DIR, exist_ok=True)

def gerar_qr_code(texto, caminho_arquivo):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(caminho_arquivo)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_path = None
    if request.method == "POST":
        texto = request.form["texto"]
        nome_arquivo = f"{uuid.uuid4().hex}.png"
        caminho_arquivo = os.path.join(QR_DIR, nome_arquivo)
        gerar_qr_code(texto, caminho_arquivo)
        qr_path = f"/{caminho_arquivo}"  # caminho acessível pela web

    return render_template("index.html", qr_path=qr_path)

#if __name__ == "__main__":
#   app.run(debug=True)

