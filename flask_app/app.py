from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
import json

# Inicializar a aplicação Flask
app = Flask(__name__)

# Função para obter uma nova conexão com o banco de dados
def get_db_connection():
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
    with open("flask_app/perfil.json", encoding='utf-8', errors='ignore') as f:
        vereadores = json.load(f)
 
    # Extraindo todos os vereadores para exibição
    vereadores_list = [
        {
            'id': int(id_),
            'nome_civil': v['nome_civil'],
            'partido': v['partido'],
            'foto': v['foto']
        }
        for id_, v in vereadores.items()
    ]
 
    return render_template("menu.html", vereadores=vereadores_list)
 
 

@app.route("/estatisticas")
def estatisticas():
    return render_template("estatisticas.html")

@app.route("/perfil/<int:id_vereador>")
def perfil(id_vereador):
    try:
        with open("flask_app/perfil.json", encoding='utf-8') as f:
            vereadores = json.load(f)
        vereador = vereadores.get(str(id_vereador))

        if vereador:
            return render_template("perfil.html", vereador=vereador)
        else:
            return "Vereador não encontrado", 404
    except Exception as e:
        return f"Erro ao carregar o perfil do vereador: {e}", 500

@app.route('/perfil/filtros')
def filtros_vereador():
    vereador_id = request.args.get('vereador_id')
    filtro = request.args.get('filtro')

    try:
        # Carregar os arquivos JSON
        with open('flask_app/leis_aprovadas_vereadores.json', encoding='utf-8') as file:
            leis_aprovadas = json.load(file)

        with open('flask_app/perfil.json', encoding='utf-8') as file:
            perfil = json.load(file)

        response_data = {}

        if filtro == 'projetos_aprovados':
            projetos_aprovados = leis_aprovadas.get(str(vereador_id), [])
            print(f"Projetos aprovados para vereador {vereador_id}: {projetos_aprovados}")
            response_data['projetos_aprovados'] = projetos_aprovados if projetos_aprovados else "Nenhum projeto aprovado encontrado para este vereador."

        elif filtro == 'biografia':
            biografia = perfil.get(str(vereador_id), {}).get('biografia', "Informação biográfica não disponível")
            print(f"Biografia do vereador {vereador_id}: {biografia}")
            response_data['biografia'] = biografia

        return jsonify(response_data)

    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return jsonify({"error": "Erro ao carregar informações."}), 500


@app.route("/propo")
def propo():
    return render_template("proposicoes2.html")

@app.route("/sobre_nos")
def sobre_nos():
    return render_template("sobre_nos.html")

# Rota para exibir os comentários com filtros e para inserir novos comentários
@app.route("/comentarios", methods=["GET", "POST"])
def comentarios():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        comentario = request.form['comentario']
        vereador_id = request.form.get('vereador_id')
        partido_id = request.form.get('partido_id')
        comissao_id = request.form.get('comissao_id')

        if not vereador_id and not partido_id and not comissao_id:
            return "Erro: Pelo menos um filtro (vereador, partido ou comissão) deve ser preenchido."

        cursor.execute("""
            INSERT INTO comentarios (comentario, vereador_id, partido_id, comissao_id)
            VALUES (%s, %s, %s, %s)
        """, (comentario, vereador_id, partido_id, comissao_id))
        db.commit()
        cursor.close()
        db.close()

        return redirect("/comentarios")

    else:
        cursor.execute("SELECT id, nome FROM vereadores")
        vereadores = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM partidos")
        partidos = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM comissoes")
        comissoes = cursor.fetchall()

        cursor.execute("SELECT * FROM comentarios")
        comentarios = cursor.fetchall()

        cursor.close()
        db.close()

        return render_template("comentarios.html", vereadores=vereadores, partidos=partidos, comissoes=comissoes, comentarios=comentarios)

# Rota para aplicar os filtros nos comentários
@app.route("/comentarios_filtro", methods=["GET"])
def comentarios_filtro():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    vereador_id = request.args.get('vereador_id')
    partido_id = request.args.get('partido_id')
    comissao_id = request.args.get('comissao_id')

    query = "SELECT * FROM comentarios WHERE 1=1"
    params = []

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

    cursor.execute("SELECT id, nome FROM vereadores")
    vereadores = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM partidos")
    partidos = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM comissoes")
    comissoes = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("comentarios.html", comentarios=comentarios, vereadores=vereadores, partidos=partidos, comissoes=comissoes)

# Rodar a aplicação
if __name__ == "__main__":
    app.run(debug=True)
