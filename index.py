from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Dados de conexão ao banco de dados
dbname = "rpg"
user = "nome_do_user"
password = "senha"
host = "localhost"
port = "5432"

def conectar_banco():
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    try:
        # Estabelecer conexão com o banco de dados
        conn = conectar_banco()

        # Criar um cursor para executar operações no banco de dados
        cursor = conn.cursor()

        # Inserir dados na tabela "usuarios"
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        
        # Confirmar a transação
        conn.commit()

        return redirect(url_for('login'))

    except psycopg2.Error as e:
        return f"Erro ao conectar ao banco de dados: {e}"
    
    finally:
        # Fechar conexão
        if conn is not None:
            conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            # Estabelecer conexão com o banco de dados
            conn = conectar_banco()

            # Criar um cursor para executar operações no banco de dados
            cursor = conn.cursor()

            # Verificar se o email e senha existem na tabela "usuarios"
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
            usuario = cursor.fetchone()

            if usuario:
                # Usuário autenticado, redirecionar para a página de sucesso
                return redirect(url_for('combatentes'))
            else:
                # Usuário não autenticado, redirecionar de volta para a página de login
                return render_template('login.html', mensagem="Credenciais inválidas. Tente novamente.")

        except psycopg2.Error as e:
            return f"Erro ao conectar ao banco de dados: {e}"
        
        finally:
            # Fechar conexão
            if conn is not None:
                conn.close()

    return render_template('login.html')

@app.route('/combatentes')
def combatentes():
    try:
        # Estabelecer conexão com o banco de dados
        conn = conectar_banco()

        # Criar um cursor para executar operações no banco de dados
        cursor = conn.cursor()

        # Selecionar todos os combatentes da tabela "combatentes"
        cursor.execute("SELECT * FROM combatentes")
        combatentes = cursor.fetchall()

        return render_template('combatentes.html', combatentes=combatentes)

    except psycopg2.Error as e:
        return f"Erro ao conectar ao banco de dados: {e}"
    
    finally:
        # Fechar conexão
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
