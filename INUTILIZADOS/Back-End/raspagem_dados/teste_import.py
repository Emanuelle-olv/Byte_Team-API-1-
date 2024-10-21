import requests # type: ignore
import PyPDF2 # type: ignore
import re
import json

# Função para baixar o PDF
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"/nPDF baixado e salvo como {filename}/n")

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Função para raspagem dos dados
def scrape_voting_data(text):
    # Expressões regulares para encontrar as seções de votação
    proposicao_regex = re.compile(r'Projeto de (Lei|Moções|Requerimentos) nº \d+')
    autor_regex = re.compile(r'Autoria: Ver\.[ª]? (.+)')
    resultado_regex = re.compile(r'Resultado: (.+)')
    votos_regex = re.compile(r'(\w+ \w+|\w+) (Favorável|Contrário|Abstenção|Presidente\*)')
    
    proposicoes = []
    proposicao = {}
    
    lines = text.split('\n')
    for line in lines:
        # Detecta um novo projeto de lei/moção/requerimento
        proposicao_match = proposicao_regex.search(line)
        if proposicao_match:
            if proposicao:
                proposicoes.append(proposicao)  # Adiciona o último projeto à lista
            proposicao = {"projeto": proposicao_match.group(), "votos": []}
        
        # Encontra a autoria
        autor_match = autor_regex.search(line)
        if autor_match:
            proposicao["autor"] = autor_match.group(1)
        
        # Encontra o resultado da votação
        resultado_match = resultado_regex.search(line)
        if resultado_match:
            proposicao["resultado"] = resultado_match.group(1)
        
        # Encontra os votos dos vereadores
        voto_match = votos_regex.findall(line)
        if voto_match:
            for vereador, voto in voto_match:
                # Transformar nome de vereador em ID
                vereador_id = vereador.replace(' ', '_').lower()
                proposicao["votos"].append({"vereador_id": vereador_id, "voto": voto})
    
    # Adiciona a última proposição
    if proposicao:
        proposicoes.append(proposicao)
    
    return proposicoes

# Função para salvar em JSON
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"/n Dados salvos em {filename} /n")

# URL do PDF e nome do arquivo a ser salvo
pdf_url = 'https://camarasempapel.camarasjc.sp.gov.br/spl/sessoes.aspx?arquivo_tipo=Extrato%20da%20Vota%c3%a7%c3%a3o%20Eletr%c3%b4nica'
pdf_filename = 'votacao.pdf'
json_filename = 'dados_votacao.json'

# Executa o download, extração e raspagem
print('/n Inicia codigo /n')
download_pdf(pdf_url, pdf_filename)
pdf_text = extract_text_from_pdf(pdf_filename)
voting_data = scrape_voting_data(pdf_text)

# Salva os dados em JSON
save_to_json(voting_data, json_filename)
