@app.route("/perfil/<int:id_vereador>")
def perfil(id_vereador):
    try:
        with open("flask_app/perfil.json", encoding='utf-8') as f:
            vereadores = json.load(f)
        vereador = vereadores.get(str(id_vereador))

        if vereador:
            filtro = request.args.get('filtro', 'projetos_aprovados')
            return render_template("perfil.html", vereador=vereador, filtro=filtro)
        else:
            return "Vereador não encontrado", 404
    except Exception as e:
        return f"Erro ao carregar o perfil do vereador: {e}", 500
