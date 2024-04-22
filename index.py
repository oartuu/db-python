from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Dados de conexão ao banco de dados
dbname = "teste"
user = "postgres"
password = "sport1987"
host = "localhost"
port = "5432"

# Consultas para cada etapa do jogo
consultas_etapas = [
    "SELECT * FROM combatentes WHERE habilidade = 'Velocidade';",
    "SELECT * FROM combatentes WHERE habilidade = 'Camuflagem';",
    "SELECT * FROM combatentes WHERE habilidade = 'Força';"
]

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
                return redirect(url_for('etapa', numero_etapa=1))
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

@app.route('/etapa/<int:numero_etapa>', methods=['GET', 'POST'])
def etapa(numero_etapa):
    if request.method == 'POST':
        consulta_usuario = request.form['consulta']
        consulta_correta = consultas_etapas[numero_etapa - 1]  # Índice começa em 0

        if consulta_usuario.strip().lower() == consulta_correta.lower():
            try:
                # Estabelecer conexão com o banco de dados
                conn = conectar_banco()

                # Criar um cursor para executar operações no banco de dados
                cursor = conn.cursor()

                # Executa a consulta no banco de dados
                cursor.execute(consultas_etapas[numero_etapa - 1])  # Substitui a consulta dinâmica
                resultados = cursor.fetchall()

                proxima_etapa = numero_etapa + 1 if numero_etapa < len(consultas_etapas) else None

                return render_template('resultado.html', resultados=resultados, etapa=numero_etapa, proxima_etapa=proxima_etapa)
            except psycopg2.Error as e:
                return f"Erro ao conectar ao banco de dados: {e}"
            finally:
                # Fechar conexão
                if conn is not None:
                    conn.close()
        else:
            return render_template('etapa.html', etapa=numero_etapa, erro=True)

    return render_template('etapa.html', etapa=numero_etapa)

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
    app.run(host='0.0.0.0')
