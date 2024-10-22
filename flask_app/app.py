from flask import Flask, render_template, request, redirect
import mysql.connector
import json

# Inicializar a aplicação Flask
app = Flask(__name__)

# Função para obter uma nova conexão com o banco de dados
def get_db_connection():
    # Abre uma nova conexão com o banco de dados sempre que necessário
    return mysql.connector.connect(
        host="localhost",
        user="apibyte",
        password="190@Mudar",
        database="apibyte",
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )

# Rotas já existentes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/estatisticas")
def estatisticas():
    return render_template("estatisticas.html")

@app.route("/perfil/<int:id_vereador>")
def perfil(id_vereador):
    with open("flask_app/perfil.json") as f:
        vereadores = json.load(f)
    
    vereador = vereadores.get(str(id_vereador))
    
    if vereador:
        return render_template("perfil.html", vereador=vereador)
    else:
        return "Vereador não encontrado", 404

@app.route("/propo")
def propo():
    return render_template("proposicoes2.html")

@app.route("/sobre_nos")
def sobre_nos():
    return render_template("sobre_nos.html")

# Rota para exibir os comentários com filtros e para inserir novos comentários
@app.route("/comentarios", methods=["GET", "POST"])
def comentarios():
    # Abre uma conexão com o banco de dados
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Se o método for POST, insere um novo comentário
    if request.method == "POST":
        comentario = request.form['comentario']
        vereador_id = request.form.get('vereador_id')
        partido_id = request.form.get('partido_id')
        comissao_id = request.form.get('comissao_id')

        # Verifica se ao menos um filtro foi preenchido
        if not vereador_id and not partido_id and not comissao_id:
            return "Erro: Pelo menos um filtro (vereador, partido ou comissão) deve ser preenchido."

        # Insere o comentário no banco de dados
        cursor.execute("""
            INSERT INTO comentarios (comentario, vereador_id, partido_id, comissao_id)
            VALUES (%s, %s, %s, %s)
        """, (comentario, vereador_id, partido_id, comissao_id))
        db.commit()

        # Fecha a conexão
        cursor.close()
        db.close()

        return redirect("/comentarios")

    # Se for GET, renderiza a página de comentários com os filtros
    else:
        # Carregar vereadores, partidos e comissões para os dropdowns
        cursor.execute("SELECT id, nome FROM vereadores")
        vereadores = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM partidos")
        partidos = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM comissoes")
        comissoes = cursor.fetchall()

        # Selecionar todos os comentários (sem filtro)
        cursor.execute("SELECT * FROM comentarios")
        comentarios = cursor.fetchall()

        # Fecha a conexão
        cursor.close()
        db.close()

        return render_template("comentarios.html", vereadores=vereadores, partidos=partidos, comissoes=comissoes, comentarios=comentarios)

# Rota para aplicar os filtros nos comentários
@app.route("/comentarios_filtro", methods=["GET"])
def comentarios_filtro():
    # Abre uma conexão com o banco de dados
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Filtros
    vereador_id = request.args.get('vereador_id')
    partido_id = request.args.get('partido_id')
    comissao_id = request.args.get('comissao_id')

    # Query básica para selecionar todos os comentários
    query = "SELECT * FROM comentarios WHERE 1=1"
    params = []

    # Adicionar filtros à query conforme preenchido
    if vereador_id:
        query += " AND vereador_id = %s"
        params.append(vereador_id)
    if partido_id:
        query += " AND partido_id = %s"
        params.append(partido_id)
    if comissao_id:
        query += " AND comissao_id = %s"
        params.append(comissao_id)

    cursor.execute(query, params)
    comentarios = cursor.fetchall()

    # Carregar vereadores, partidos e comissões para os dropdowns
    cursor.execute("SELECT id, nome FROM vereadores")
    vereadores = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM partidos")
    partidos = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM comissoes")
    comissoes = cursor.fetchall()

    # Fecha a conexão
    cursor.close()
    db.close()

    # Renderizar a página com os comentários filtrados
    return render_template("comentarios.html", comentarios=comentarios, vereadores=vereadores, partidos=partidos, comissoes=comissoes)

# Rodar a aplicação
if __name__ == "__main__":
    app.run(debug=True)
