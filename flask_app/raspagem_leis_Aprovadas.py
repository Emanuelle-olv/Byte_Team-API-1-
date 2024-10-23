import requests
from bs4 import BeautifulSoup
import json

# URL correta da página
url = "https://camarasempapel.camarasjc.sp.gov.br/legislacao/consulta-legislacao.aspx?tipo=22&situacao=3&modo=S&interno=0&autor=1274&inicio=01%2f01%2f2021"

# Cabeçalhos para a requisição (imitando um navegador)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Fazendo a requisição HTTP
response = requests.get(url, headers=headers)

# Verificando se a resposta foi bem-sucedida
if response.status_code == 200:
    print(f"Acessando a página com sucesso: {url}")

    # Fazendo o parsing do HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Aqui está o JSON onde os dados serão armazenados
    leis = []

    # Inspecionar a página para pegar os elementos corretos
    # Exemplo de extração de informações como título, número e data
    items = soup.find_all("div", class_="kt-widget5__item")

    for item in items:
        title = item.find("a", class_="kt-widget5__title").get_text(strip=True)
        descricao = item.find("a", class_="kt-widget5__desc").get_text(strip=True)
        data = item.find("span", class_="kt-font-info").get_text(strip=True)
        link_detalhes = item.find("a", class_="kt-widget5__title")["href"]

        # Salvando os dados coletados em um dicionário
        lei = {
            "titulo": title,
            "descricao": descricao,
            "data": data,
            "link_detalhes": f"https://camarasempapel.camarasjc.sp.gov.br/{link_detalhes}",
        }

        leis.append(lei)

    # Salvando em um arquivo JSON
    with open("leis_ordinarias_Ze_Luiz.json", "w", encoding="utf-8") as f:
        json.dump(leis, f, ensure_ascii=False, indent=4)

    print("Dados raspados e salvos com sucesso!")

else:
    print(f"Erro ao acessar a página: {response.status_code}")
