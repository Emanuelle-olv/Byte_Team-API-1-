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
        charset="utf8mb4",
        collation="utf8mb4_general_ci",
    )


# Rotas já existentes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    with open("perfil.json", encoding="utf-8", errors="ignore") as f:
        vereadores = json.load(f)

    # Extraindo todos os vereadores para exibição
    vereadores_list = [
        {
            "id": int(id_),
            "nome_civil": v["nome_civil"],
            "partido": v["partido"],
            "foto": v["foto"],
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
        with open("perfil.json", encoding="utf-8") as f:
            vereadores = json.load(f)
        vereador = vereadores.get(str(id_vereador))

        if vereador:
            filtro = request.args.get('filtro', 'projetos_aprovados')
            return render_template("perfil.html", vereador=vereador, filtro=filtro)
        else:
            return "Vereador não encontrado", 404
    except Exception as e:
        return f"Erro ao carregar o perfil do vereador: {e}", 500

@app.route('/perfil/filtros')
def filtros_vereador():
    vereador_id = request.args.get("vereador_id")
    filtro = request.args.get("filtro")

    try:
        with open("leis_aprovadas_vereadores.json", encoding="utf-8") as file:
            leis_aprovadas = json.load(file)

        with open("perfil.json", encoding="utf-8") as file:
            perfil = json.load(file)

        comissoes_validas = [
            (37, "Comissão de Cultura e Esportes"),
            (43, "Comissão de Economia, Finanças e Orçamento"),
            (26, "Comissão de Educação e Promoção Social"),
            (40, "Comissão de Ética"),
            (39, "Comissão de Justiça, Redação e Direitos Humanos"),
            (42, "Comissão de Meio Ambiente"),
            (41, "Comissão de Planejamento Urbano, Obras e Transportes"),
            (38, "Comissão de Saúde"),
        ]
        comissoes_dict = {str(id): nome for id, nome in comissoes_validas}

        response_data = {}

        if filtro == "projetos_aprovados":
            projetos_aprovados = leis_aprovadas.get(str(vereador_id), [])
            response_data["projetos_aprovados"] = (
                projetos_aprovados
                if projetos_aprovados
                else "Nenhum projeto aprovado encontrado para este vereador."
            )

        elif filtro == "biografia":
            biografia = perfil.get(str(vereador_id), {}).get(
                "biografia", "Informação biográfica não disponível"
            )
            response_data["biografia"] = biografia

        elif filtro == "frequencia_sessoes":
            frequencia = perfil.get(str(vereador_id), {})
            response_data["frequencia"] = {
                "presenca_totais": frequencia.get("presenca_totais", "N/A"),
                "presenca_2021": frequencia.get("presenca_2021", "N/A"),
                "presenca_2022": frequencia.get("presenca_2022", "N/A"),
                "presenca_2023": frequencia.get("presenca_2023", "N/A"),
                "presenca_2024": frequencia.get("presenca_2024", "N/A"),
                "faltas_totais": frequencia.get("faltas_totais", "N/A"),
                "faltas_2021": frequencia.get("faltas_2021", "N/A"),
                "faltas_2022": frequencia.get("faltas_2022", "N/A"),
                "faltas_2023": frequencia.get("faltas_2023", "N/A"),
                "faltas_2024": frequencia.get("faltas_2024", "N/A"),
                "faltas_justificadas_totais": frequencia.get(
                    "faltas_justificadas_totais", "N/A"
                ),
                "faltas_justificadas_2021": frequencia.get(
                    "faltas_justificadas_2021", "N/A"
                ),
                "faltas_justificadas_2022": frequencia.get(
                    "faltas_justificadas_2022", "N/A"
                ),
                "faltas_justificadas_2023": frequencia.get(
                    "faltas_justificadas_2023", "N/A"
                ),
                "faltas_justificadas_2024": frequencia.get(
                    "faltas_justificadas_2024", "N/A"
                ),
            }

        elif filtro == "proposicoes":
            proposicoes = perfil.get(str(vereador_id), {})
            response_data["proposicoes"] = {
                "mocoes": proposicoes.get("mocoes", "N/A"),
                "projeto_de_lei": proposicoes.get("projeto_de_lei", "N/A"),
                "projeto_de_lei_aprovados": proposicoes.get(
                    "projeto_de_lei_aprovados", "N/A"
                ),
                "requerimento": proposicoes.get("requerimento", "N/A"),
            }

        elif filtro == "comissoes":
            comissoes_anos = {
                "2021": perfil.get(str(vereador_id), {}).get(
                    "comissoes_atuantes_2021_id", []
                ),
                "2022": perfil.get(str(vereador_id), {}).get(
                    "comissoes_atuantes_2022_id", []
                ),
                "2023": perfil.get(str(vereador_id), {}).get(
                    "comissoes_atuantes_2023_id", []
                ),
                "2024": perfil.get(str(vereador_id), {}).get(
                    "comissoes_atuantes_2024_id", []
                ),
            }

            comissoes_final = {}
            for ano, comissoes in comissoes_anos.items():
                if comissoes:  # Verifica se há comissões
                    nomes_comissoes = [
                        comissoes_dict.get(
                            str(comissao_id),
                            f"Comissão ID {comissao_id} não encontrada",
                        )
                        for comissao_id in comissoes
                    ]
                    comissoes_final[ano] = nomes_comissoes

            response_data["comissoes"] = comissoes_final

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
        comentario = request.form["comentario"]
        vereador_id = request.form.get("vereador_id")
        partido_id = request.form.get("partido_id")
        comissao_id = request.form.get("comissao_id")

        if not vereador_id and not partido_id and not comissao_id:
            return "Erro: Pelo menos um filtro (vereador, partido ou comissão) deve ser preenchido."

        cursor.execute(
            """
            INSERT INTO comentarios (comentario, vereador_id, partido_id, comissao_id)
            VALUES (%s, %s, %s, %s)
        """,
            (comentario, vereador_id, partido_id, comissao_id),
        )
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

        return render_template(
            "comentarios.html",
            vereadores=vereadores,
            partidos=partidos,
            comissoes=comissoes,
            comentarios=comentarios,
        )


# Rota para aplicar os filtros nos comentários
@app.route("/comentarios_filtro", methods=["GET"])
def comentarios_filtro():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    vereador_id = request.args.get("vereador_id")
    partido_id = request.args.get("partido_id")
    comissao_id = request.args.get("comissao_id")

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

    return render_template(
        "comentarios.html",
        comentarios=comentarios,
        vereadores=vereadores,
        partidos=partidos,
        comissoes=comissoes,
    )


# Rodar a aplicação
if __name__ == "__main__":
    app.run(debug=True)
