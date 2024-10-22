# Use uma imagem base com Python
FROM python:3.12

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências listadas no requirements.txt
RUN pip install -r requirements.txt

# Copie todo o código para o diretório de trabalho no contêiner
COPY . .

# Defina a porta que o Flask irá usar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "flask_app/app.py"]
