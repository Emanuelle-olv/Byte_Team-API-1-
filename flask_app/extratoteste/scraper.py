import re
import json
import PyPDF2
import os

# Caminho da pasta onde os PDFs estão localizados
pasta_pdf = r'flask_app\extratoteste'  # Substitua pelo caminho correto da sua pasta

# Verificar todos os arquivos na pasta e pegar apenas os PDFs
arquivos_pdf = [f for f in os.listdir(pasta_pdf) if f.endswith('.pdf')]

# Nome do arquivo JSON onde os dados serão armazenados
json_file_path = r'flask_app\extratos_votacao.json'

# Verificar se o arquivo JSON já existe
if os.path.exists(json_file_path):
    # Se o arquivo existir, carregar os dados existentes
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        try:
            dados_existentes = json.load(json_file)
        except json.JSONDecodeError:
            # Se o arquivo estiver vazio ou corrompido, inicializar como lista vazia
            dados_existentes = []
else:
    # Se o arquivo não existir, iniciar uma nova lista
    dados_existentes = []

# Dicionário de correspondência de nomes para IDs (sem "id", apenas números)
nomes_para_ids = {
    "lia Naomi": "001",
    "Claudio": "002",
    "Dulce Rita": "003",
    "o Zagueiro": "004",
    "Fernando Petiti": "005",
    "Juliana Fraga": "006",
    "rio": "007",
    "cia": "008",
    "Lino Bispo": "009",
    "o da Academia": "010",
    "Marcelo Garcia": "011",
    "Milton Vieira Filho": "012",
    "Rafael Pascucci": "013",
    "Renato Santiago": "014",
    "Robertinho da Padaria": "015",
    "Roberto Chagas": "016",
    "rio da ACASEM": "017",
    "Thomaz Henrique": "018",
    "Walter Hayashi": "019",
    "Luis": "020",
    "Roberto do Eleven": "021"
}

# Loop por todos os arquivos PDF na pasta
for pdf_file in arquivos_pdf:
    caminho_completo = os.path.join(pasta_pdf, pdf_file)

    # Abrir o arquivo PDF
    with open(caminho_completo, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Extrair todo o texto do PDF
        texto = ''
        for page in reader.pages:
            texto += page.extract_text()

    # Padrões para capturar os títulos, resultados e votos
    padrao_titulo = re.compile(r"(\d+\)) (Votação.*?|Moção.*?|Requerimento.*?|Emenda.*?|Projeto de Lei.*?)(?:\n|\r)")  # Captura o título
    padrao_resultado = re.compile(r"Resultado: (Aprovado|Rejeitado)")
    padrao_votacao = re.compile(r"([A-Za-z\s\.]+) (Favorável|Contrário|Abstenção)")

    # Vamos organizar as informações em uma lista
    extratos = []
    titulos = padrao_titulo.findall(texto)
    resultados = padrao_resultado.findall(texto)

    # Garantir que cada extrato seja processado apenas uma vez
    titulos_unicos = list(dict.fromkeys(titulos))  # Remove duplicatas mantendo a ordem

    # Captura o índice de onde cada título aparece para processar separadamente
    for i, (numero, titulo) in enumerate(titulos_unicos):
        # Capturar o resultado correspondente ao título
        resultado = resultados[i] if i < len(resultados) else 'Desconhecido'
        
        # Captura o bloco de texto correspondente à sessão atual
        inicio_votacao = texto.index(titulo)
        if i + 1 < len(titulos_unicos):
            proximo_titulo = titulos_unicos[i + 1][1]  # O título da próxima votação
            fim_votacao = texto.index(proximo_titulo)
            sessao_texto = texto[inicio_votacao:fim_votacao]
        else:
            sessao_texto = texto[inicio_votacao:]
        
        # Captura os votos para essa sessão
        votos = padrao_votacao.findall(sessao_texto)
        
        # Estrutura os dados com substituição de nomes por IDs (apenas números)
        votacao = {
            'titulo': titulo.strip(),
            'resultado': resultado,
            'votos': [{'id': nomes_para_ids.get(nome.strip(), nome.strip()), 'voto': voto} for nome, voto in votos]
        }
        extratos.append(votacao)

    # Adicionar os novos dados à lista de dados existentes
    dados_existentes.extend(extratos)

# Salvar todos os dados (antigos + novos) no arquivo JSON
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(dados_existentes, json_file, ensure_ascii=False, indent=4)

print(f"Dados extraídos de todos os arquivos PDF na pasta '{pasta_pdf}' e salvos no arquivo {json_file_path}")
