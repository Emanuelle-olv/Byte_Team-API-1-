from flask import Flask, render_template

# Inicializar a aplicação Flask
app = Flask(__name__)

# Rota para a página inicial (index)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de menu
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Rota para a página de estatísticas
@app.route('/estatisticas')
def estatisticas():
    return render_template('estatisticas.html')

# Rota para a página de perfil
@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

# Rota para a página de proposições
@app.route('/propo')
def propo():
    return render_template('propo.html')

# Rota para a página sobre nós
@app.route('/sobre_nos')
def sobre_nos():
    return render_template('sobre_nos.html')

# Rodar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
