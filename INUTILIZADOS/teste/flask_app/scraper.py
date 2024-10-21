import os
import requests
from PIL import Image
from io import BytesIO

# URL da API
url = 'https://camarasempapel.camarasjc.sp.gov.br//api/publico/parlamentar/?pg=1&qtd=100'

# Fazendo a requisição à API
response = requests.get(url)
data = response.json()

# Imprimir a estrutura do JSON para verificar
print(data)  # Isso vai exibir a resposta da API para que possamos verificar a estrutura

# Criando um diretório para armazenar as fotos, se não existir
if not os.path.exists('static/fotos_vereadores'):
    os.makedirs('static/fotos_vereadores')

# Iterando sobre os vereadores para baixar as fotos
# O loop só será ajustado quando verificarmos a estrutura correta da resposta
for vereador in data:  # Pode precisar ajustar o caminho aqui com base no print acima
    vereador_id = vereador['idParlamentar']  # Verifique se 'idParlamentar' é a chave correta
    foto_url = vereador['foto']  # Verifique se 'foto' é a chave correta para o link da imagem

    # Requisição para baixar a imagem
    foto_response = requests.get(foto_url)
    
    # Carregando a imagem
    img = Image.open(BytesIO(foto_response.content))
    
    # Salvando a imagem com o ID do vereador
    img.save(f"static/fotos_vereadores/{vereador_id}.jpg")

print("Fotos dos vereadores baixadas e salvas com sucesso!")
