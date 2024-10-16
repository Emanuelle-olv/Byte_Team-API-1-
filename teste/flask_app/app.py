from flask import Flask, render_template, send_file
import json  # Para trabalhar com arquivos JSON
import pandas as pd  # Para organizar e analisar dados
import matplotlib.pyplot as plt  # Para criar gráficos
from io import BytesIO  # Para salvar gráficos no formato de bytes
import os  # Para verificar se o arquivo existe

# Inicializar a aplicação Flask
app = Flask(__name__)

# Função para ler dados de arquivos JSON
def ler_dados_json(arquivo_json):
    """
    Lê os dados de um arquivo JSON e retorna um dicionário.
    O arquivo JSON é passado como argumento.
    """
    if not os.path.exists(arquivo_json):
        print(f"Erro: O arquivo {arquivo_json} não foi encontrado.")
        return {}  # Retorna um dicionário vazio se o arquivo não for encontrado
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    return dados

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

# Rota para o perfil individual de cada vereador
@app.route('/perfil/<int:id_vereador>')
def perfil_vereador(id_vereador):
    """
    Carrega os dados do 'perfil.json' e exibe o perfil do vereador correspondente ao ID.
    """
    dados = ler_dados_json('perfil.json')  # Lê os dados do arquivo 'perfil.json'
    vereador = dados.get(str(id_vereador), None)  # Busca pelo ID do vereador no dicionário

    if vereador:
        return render_template('perfil.html', vereador=vereador)
    else:
        return "Vereador não encontrado", 404  # Retorna um erro 404 se o vereador não for encontrado

# Rota para exibir todos os vereadores
@app.route('/vereadores')
def todos_vereadores():
    """
    Carrega os dados do 'vereadores.json' e exibe todos os vereadores.
    """
    dados = ler_dados_json('vereadores.json')  # Lê os dados do arquivo 'vereadores.json'
    return render_template('vereadores.html', vereadores=dados)

# Rota para a página de proposições
@app.route('/propo')
def propo():
    return render_template('propo.html')

# Rota para a página sobre nós
@app.route('/sobre_nos')
def sobre_nos():
    return render_template('sobre_nos.html')

# Rota para gerar um gráfico de distribuição de vereadores por partido
@app.route('/grafico_partido')
def grafico_partido():
    """
    Gera e exibe um gráfico de barras com a distribuição de vereadores por partido.
    """
    # Lê os dados do arquivo 'todos_vereadores.json'
    dados = ler_dados_json('todos_vereadores.json')

    # Converte os dados para um DataFrame do Pandas
    df = pd.DataFrame(dados).T  # .T para transpor e organizar os dados corretamente

    # Verifica se o DataFrame está vazio para evitar erros ao gerar o gráfico
    if df.empty:
        return "Nenhum dado disponível para gerar gráficos", 404

    # Cria o gráfico de distribuição por partido
    partido_counts = df['partido'].value_counts()  # Conta a quantidade de vereadores por partido
    plt.figure(figsize=(8, 6))  # Define o tamanho do gráfico
    partido_counts.plot(kind='bar', color='blue')  # Gera o gráfico de barras
    plt.title('Distribuição de Vereadores por Partido')  # Título do gráfico
    plt.xlabel('Partido')  # Legenda do eixo X
    plt.ylabel('Número de Vereadores')  # Legenda do eixo Y

    # Salva o gráfico em um buffer de bytes para ser enviado como resposta
    img = BytesIO()  # Cria um buffer de bytes em memória
    plt.savefig(img, format='png')  # Salva o gráfico no formato PNG
    img.seek(0)  # Move o cursor para o início do buffer
    plt.close()  # Fecha o gráfico para liberar a memória

    # Envia o gráfico gerado como uma imagem PNG para ser exibido no navegador
    return send_file(img, mimetype='image/png')

# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
