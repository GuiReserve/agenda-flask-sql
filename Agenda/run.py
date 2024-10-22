from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
 
# Certifique-se de que a pasta de upload exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
 
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route("/enviar", methods=['POST'])
def enviar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
 
    if 'imagem' not in request.files:
        imagem_filename = None
    else:
        imagem = request.files['imagem']
        if imagem.filename != '':
            imagem_filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename))
        else:
            imagem_filename = None
 
 
    conexao = sqlite3.connect('models/agenda.db')
    cursor = conexao.cursor()
   
    sql = 'INSERT INTO tb_pessoas (nome, email, telefone, imagem) VALUES (?, ?, ?, ?)'
    cursor.execute(sql, (nome, email, telefone, imagem_filename))
   
    conexao.commit()
    conexao.close()
   
    return redirect('/')
 
@app.route('/consulta')
def consulta():
    conexao = sqlite3.connect('models/agenda.db')
    cursor = conexao.cursor()
 
    sql = 'SELECT * FROM tb_pessoas'
    cursor.execute(sql)
    pessoas = cursor.fetchall()
   
    conexao.close()
 
    return render_template('consulta.html', pessoas=pessoas)
 
@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    conexao = sqlite3.connect('models/agenda.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_pessoas WHERE pessoa_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consulta')
 
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conexao = sqlite3.connect('models/agenda.db')
    cursor = conexao.cursor()
 
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
       
        if 'imagem' in request.files and request.files['imagem'].filename != '':
            imagem = request.files['imagem']
            imagem_filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename))
        else:
            imagem_filename = None
 
        sql = "UPDATE tb_pessoas SET nome = ?, email = ?, telefone = ?, imagem = ? WHERE pessoa_id = ?"
        cursor.execute(sql, (nome, email, telefone, imagem_filename, id))
       
        conexao.commit()
        conexao.close()
       
        return redirect('/consulta')
    else:
        cursor.execute("SELECT * FROM tb_pessoas WHERE pessoa_id = ?", (id,))
        pessoa = cursor.fetchone()
        conexao.close()
       
        return render_template('editar.html', pessoa=pessoa)
 
app.run(host="127.0.0.1", port=80, debug=True)
 