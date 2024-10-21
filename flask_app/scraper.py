import os
import PyPDF2
import re
import json

# Lista de vereadores com seus respectivos IDs
vereadores_validos = [
    (35, 'Amélia Naomi'),
    (238, 'Dr. José Claudio'),
    (38, 'Dulce Rita'),
    (247, 'Fabião Zagueiro'),
    (40, 'Fernando Petiti'),
    (43, 'Juliana Fraga'),
    (246, 'Junior da Farmácia'),
    (44, 'Juvenil Silvério'),
    (45, 'Lino Bispo'),
    (47, 'Marcão da Academia'),
    (244, 'Marcelo Garcia'),
    (242, 'Milton Vieira Filho'),
    (243, 'Rafael Pascucci'),
    (245, 'Renato Santiago'),
    (50, 'Robertinho da Padaria'),
    (240, 'Roberto Chagas'),
    (234, 'Roberto do Eleven'),
    (249, 'Rogério da ACASEM'),
    (239, 'Thomaz Henrique'),
    (55, 'Walter Hayashi'),
    (237, 'Zé Luís')
]

# Caminho da pasta onde os PDFs estão localizados
pdf_folder = 'D:/Vinny'

# Função para extrair texto de um PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        full_text = ''
        
        # Extrair texto de cada página
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            full_text += page.extract_text()
        
        return full_text

# Função para mapear o nome do vereador ao seu ID
def map_vereador_to_id(nome_vereador):
    for id_vereador, nome in vereadores_validos:
        if nome in nome_vereador:
            return id_vereador
    return None

# Função para encontrar as informações específicas no texto
def extract_voting_data(text):
    # Regex para encontrar o número do processo, projeto de lei, moção ou requerimento
    process_number = re.search(r'[Pp]rojeto de [Ll]ei\s*nº\s*(\d+/\d+)|[Mm]oção\s*nº\s*(\d+/\d+)|[Rr]equerimento\s*nº\s*(\d+/\d+)', text)
    
    # Verifica se um número foi encontrado e armazena o valor correto
    if process_number:
        process_number = process_number.group(0)

    # Regex para encontrar a autoria (usamos os IDs em vez do nome)
    autoria_nome = re.search(r'Autoria:\s*(.*)', text)
    if autoria_nome:
        autor_id = map_vereador_to_id(autoria_nome.group(1).strip())
    else:
        autor_id = None

    # Regex para encontrar o resultado
    result = re.search(r'Resultado:\s*(.*)', text)
    
    # Regex para capturar a votação de cada vereador (nome e se foi favorável ou contrário)
    votos = re.findall(r'([A-Za-z\s]+)\s+(Favorável|Contrário)', text)

    # Organizar os votos com os IDs dos vereadores
    votos_com_ids = []
    for vereador, voto in votos:
        id_vereador = map_vereador_to_id(vereador.strip())
        if id_vereador:
            votos_com_ids.append({'id': id_vereador, 'vereador': vereador.strip(), 'voto': voto})
    
    return {
        'process_number': process_number if process_number else None,
        'authorship': autor_id,
        'result': result.group(1) if result else None,
        'votos': votos_com_ids
    }

# Processar todos os PDFs na pasta e salvar em JSON
def process_pdfs_in_folder(folder_path, json_output_path):
    all_voting_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processando {filename}...")
            
            # Extrair texto do PDF
            pdf_text = extract_text_from_pdf(pdf_path)
            
            # Extrair dados da votação
            voting_data = extract_voting_data(pdf_text)
            
            # Adicionar nome do arquivo para referência
            voting_data['filename'] = filename
            
            # Adicionar os dados ao conjunto de dados
            all_voting_data.append(voting_data)

    # Salvar todos os dados extraídos em um arquivo JSON
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_voting_data, json_file, ensure_ascii=False, indent=4)

# Caminho do arquivo de saída JSON
json_output_path = 'D:/Vinny/extratos_votacao.json'

# Processar os PDFs e salvar em JSON
process_pdfs_in_folder(pdf_folder, json_output_path)

print(f"Os dados foram salvos em {json_output_path}")
