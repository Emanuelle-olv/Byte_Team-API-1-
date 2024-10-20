import os
import requests
from PIL import Image
from io import BytesIO

# URL da API
url = 'https://camarasempapel.camarasjc.sp.gov.br//api/publico/parlamentar/?pg=1&qtd=100'

# Fazendo a requisição à API
response = requests.get(url)
data = response.json()

# Criando um diretório para armazenar as fotos, se não existir
if not os.path.exists('static/fotos_vereadores'):
    os.makedirs('static/fotos_vereadores')

# Iterando sobre os vereadores para baixar as fotos
for vereador in data['value']:
    vereador_id = vereador['idParlamentar']  # Usando o ID do vereador
    foto_url = vereador['foto']  # Assumindo que o campo da URL da foto seja 'foto'

    # Requisição para baixar a imagem
    foto_response = requests.get(foto_url)
    
    # Carregando a imagem
    img = Image.open(BytesIO(foto_response.content))
    
    # Salvando a imagem com o ID do vereador
    img.save(f"static/fotos_vereadores/{vereador_id}.jpg")

print("Fotos dos vereadores baixadas e salvas com sucesso!")
