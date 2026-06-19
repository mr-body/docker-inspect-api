FROM python:3.12-slim

WORKDIR /app

# instala docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# cria usuário
RUN groupadd -r docker-inspect && \
    useradd -r -g docker-inspect -m -d /home/docker-inspect -s /bin/bash docker-inspect

# copia código como root
COPY . .

# instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔒 remove acesso ao /app para o usuário
RUN chown -R root:root /app && \
    chmod -R 700 /app

# garante que usuário NÃO pode escrever
RUN chmod -R o-rwx /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]