from flask import Flask, request, send_from_directory, render_template, redirect, url_for
from scraper import scrape  # supondo que você tenha um módulo chamado scraper.py
import os
import webbrowser

app = Flask(__name__)

# Diretório para armazenar os arquivos temporários
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# URL da página HTML
html_page_url = "http://127.0.0.1:5000/"

# Variável para controlar se o navegador já foi aberto
navegador_aberto = False

# Função para abrir a página HTML no navegador


def abrir_pagina_html():
    global navegador_aberto
    if not navegador_aberto:
        webbrowser.open(html_page_url)
        navegador_aberto = True  # Definindo como True após abrir o navegador


# Criar o diretório 'uploads' se ele não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Chamar a função para abrir a página HTML ao iniciar o servidor Flask
abrir_pagina_html()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def handle_scrape():
    url = request.form['url']
    result = scrape(url)

    if result:
        # Salvar o arquivo temporariamente no servidor
        filename = 'dados_scraping.xlsx'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(result)

        # Redirecionar o cliente para a rota de download
        return redirect(url_for('download_file', filename=filename))
    else:
        return "Erro ao fazer scraping dos dados. Tente novamente mais tarde."


@app.route('/<path:filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
