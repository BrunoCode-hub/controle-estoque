from flask import Flask, render_template, request, redirect
from database import conectar

app = Flask(__name__,
            template_folder='front',
            static_folder='css',
            static_url_path='/estilo'

        )
# Listar Produtos
@app.route('/')
def index():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conn.close()
    return render_template('index.html', produtos=produtos)

#Formulario
@app.route('/novo')
def novo_produto():
    return render_template('novo_produto.html')

#Inserir no Banco
@app.route('/salvar', methods=['POST'])
def salvar():

    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    conn = conectar()
    cursor = conn.cursor()

    sql = "insert into produtos (nome, quantidade, preco) values (%s, %s, %s)"
    valores = (nome, quantidade, preco)
    cursor.execute(sql, valores)
    conn.commit()
    conn.close()
    return redirect('/')
app.run(debug=True)
