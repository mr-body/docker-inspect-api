# docker-inspect-api

[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

O projeto permite inspecionar e listar informações do ambiente Docker de forma simples através de endpoints HTTP. Inclui funcionalidades para consultar containers em execução, imagens, redes e volumes.

## Funcionalidades

- Listagem de containers em execução
- Consulta de imagens Docker disponíveis
- Visualização de redes Docker configuradas
- Listagem e consulta de volumes
- API HTTP simples e fácil de consumir

## Como usar

### Com Docker

Você pode rodar a aplicação facilmente usando Docker:

```bash
docker build -t docker-inspect-api .
docker run -d -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock docker-inspect-api
```

### Localmente

Certifique-se de que você possui o Docker instalado e o Python 3.8+.

1. Clone o repositório:

   ```bash
   git clone https://github.com/mr-body/docker-inspect-api.git
   cd docker-inspect-api
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:

   ```bash
   python src/main.py
   ```

## Endpoints disponíveis

- `GET /containers` – Lista containers em execução
- `GET /images` – Lista imagens Docker
- `GET /networks` – Lista redes Docker
- `GET /volumes` – Lista volumes Docker

## Requisitos

- Python 3.8+
- Docker instalado (com acesso ao socket do Docker)

## Exemplo de resposta

```json
[
  {
    "Id": "a1b2c3d4e5f6",
    "Image": "nginx:latest",
    "Status": "Up 10 minutes",
    "Names": ["nginx-server"]
  }
]
```

## Licença

MIT License

---

Desenvolvido por [mr-body](https://github.com/mr-body)
