import json
import requests
from bs4 import BeautifulSoup
import os

# Lista de IDs dos vereadores
ids_vereadores = [35, 238, 38, 247, 40, 43, 246, 44, 45, 47, 244, 242, 243, 245, 50, 240, 234, 249, 239, 55]

# Dicionário de fotos associadas aos vereadores
# Dicionário de fotos associadas aos vereadores
# Dicionário de fotos associadas aos vereadores
fotos_vereadores = {
    "35": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/70878385417st6d28o4c.jpg",
    "43": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/juliana fraga.jpg",
    "44": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/juvenil(1).jpg",
    "45": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/2684u0fw768v144jog05.jpg",
    "47": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/57efx26qj127vw845i68.jpg",
    "50": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/robertinho da padaria.jpg",
    "55": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/walter hayashi.jpg",
    "240": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/11x3521c2h31ms7o7ptt.jpg",
    "249": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/2a21q5lr71q63crryfmp.jpg",
    "38": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/os1860xrd1r4ti771ven.jpg",
    "243": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/l7v18288882yb4165183.jpg",
    "242": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/x782015ys02p1u205nyq.jpg",
    "40": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/53028hrhq7brv7l8ii14.jpg",
    "245": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/x42xbq4a20b5i0iaxhh4.jpg",
    "246": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/il43yg1ntgug436fnpja.jpg",
    "247": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/c3u085f11t2x47khu0c3.jpg",
    "239": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/d474lum2083h76wsa4om.jpg",
    "244": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/r8m57lqv4sls8uf20n7v.jpg",
    "234": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/u53b832se27kqr176cvi.jpg",
    "238": "https://camarasempapel.camarasjc.sp.gov.br/arquivo/images/pessoas/lm26puws46b58lwh7p4a.jpg"
}

# Função para baixar dados de um vereador específico
def baixar_dados_vereador(id_vereador):
    url = f"https://camarasempapel.camarasjc.sp.gov.br/spl/parlamentar.aspx?id={id_vereador}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extrair dados do vereador
        nome_civil = soup.find(text="Nome civil:").find_next().text.strip() if soup.find(text="Nome civil:") else "Nome não encontrado"
        partido = soup.find('span', {'id': 'partido'}).text.strip() if soup.find('span', {'id': 'partido'}) else "Partido não encontrado"
        telefone = soup.find(text="Telefone(s):").find_next().text.strip() if soup.find(text="Telefone(s):") else "Telefone não encontrado"
        email = soup.find(text="E-mail:").find_next().text.strip() if soup.find(text="E-mail:") else "E-mail não encontrado"

        # Pegar a URL da foto associada ao ID do vereador
        foto = fotos_vereadores.get(str(id_vereador), "Foto não encontrada")

        # Organizar os dados em um dicionário
        vereador_dados = {
            "id": id_vereador,
            "nome_civil": nome_civil,
            "partido": partido,
            "telefone": telefone,
            "email": email,
            "foto": foto
        }

        return vereador_dados
    else:
        return {"id": id_vereador, "erro": "Erro ao acessar"}

# Função para salvar os dados em um arquivo JSON
def salvar_dados_em_json(vereadores, arquivo_json):
    with open(arquivo_json, 'w') as f:
        json.dump(vereadores, f, indent=4)  # Salva o arquivo JSON de forma legível

# Função para raspar dados de todos os vereadores e salvar em arquivos JSON
def raspar_todos_os_vereadores():
    todos_vereadores = {}

    for id_vereador in ids_vereadores:
        # Baixar os dados de cada vereador
        vereador_dados = baixar_dados_vereador(id_vereador)

        # Adicionar os dados ao dicionário geral
        todos_vereadores[id_vereador] = vereador_dados

        # Feedback no console
        print(f"Dados do vereador {id_vereador} coletados com sucesso.")

    # Salvar todos os dados em um único arquivo JSON
    salvar_dados_em_json(todos_vereadores, 'todos_vereadores.json')

# Função para baixar a imagem de um vereador e salvar localmente
def baixar_imagem_vereador(id_vereador):
    url_imagem = fotos_vereadores.get(str(id_vereador))

    if url_imagem and "Foto não encontrada" not in url_imagem:
        response = requests.get(url_imagem)
        
        if response.status_code == 200:
            # Criar o diretório 'static/img' se não existir
            if not os.path.exists('static/img'):
                os.makedirs('static/img')

            # Salvar a imagem no diretório
            caminho_imagem = f'static/img/{id_vereador}.jpg'
            with open(caminho_imagem, 'wb') as f:
                f.write(response.content)

            print(f"Imagem do vereador {id_vereador} baixada com sucesso.")
        else:
            print(f"Erro ao baixar a imagem do vereador {id_vereador}")
    else:
        print(f"URL da imagem do vereador {id_vereador} não encontrada.")

# Função para baixar imagens de todos os vereadores
def baixar_todas_imagens():
    for id_vereador in ids_vereadores:
        baixar_imagem_vereador(id_vereador)

# Executar a raspagem de todos os dados e imagens
if __name__ == "__main__":
    raspar_todos_os_vereadores()
    baixar_todas_imagens()
