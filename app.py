from flask import Flask, render_template, request, redirect, session
from database import conectar

app = Flask(
    __name__,
    template_folder='front',
    static_folder='css',
    static_url_path='/estilo'
)

# Chave utilizada pelo Flask para trabalhar com sessões
app.secret_key = 'chave-secreta-estoque'


# ==========================================
# TELA DE LOGIN
# ==========================================

@app.route('/')
def login():
    return render_template('login.html')


# ==========================================
# AUTENTICAÇÃO
# ==========================================

@app.route('/autenticar', methods=['POST'])
def autenticar():

    user = request.form['usuario']
    senha = request.form['senha']

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s AND senha=%s",
        (user, senha)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:

        # Guarda o usuário na sessão
        session['usuario'] = user

        return redirect('/produtos')

    else:
        return "Login inválido"


# ==========================================
# LISTAR PRODUTOS
# ==========================================

@app.route('/produtos')
def index():

    # Verifica se o usuário está logado
    if 'usuario' not in session:
        return redirect('/')

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")

    produtos = cursor.fetchall()

    conn.close()

    return render_template('index.html', produtos=produtos)


# ==========================================
# FORMULÁRIO NOVO PRODUTO
# ==========================================

@app.route('/novo')
def novo_produto():

    # Verifica se o usuário está logado
    if 'usuario' not in session:
        return redirect('/')

    return render_template('novo_produto.html')


# ==========================================
# INSERIR PRODUTO NO BANCO
# ==========================================

@app.route('/salvar', methods=['POST'])
def salva():

    # Verifica se o usuário está logado
    if 'usuario' not in session:
        return redirect('/')

    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO produtos(nome, quantidade, preco)
        VALUES (%s, %s, %s)
    """

    valores = (nome, quantidade, preco)

    cursor.execute(sql, valores)

    conn.commit()

    conn.close()

    return redirect('/produtos')


# ==========================================
# LOGOUT
# ==========================================

@app.route('/logout')
def logout():

    # Remove os dados da sessão
    session.clear()

    return redirect('/')


# ==========================================
# INICIAR APLICAÇÃO
# ==========================================

app.run(debug=True)