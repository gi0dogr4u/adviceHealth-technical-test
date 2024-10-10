# City Car Management

Este projeto é um sistema de gerenciamento de carros para a cidade fictícia de Nork-Town. O sistema permite adicionar proprietários de carros e gerenciar os carros registrados a cada um deles.

## Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)


## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/gi0dogr4u/adviceHealth-technical-test.git
   cd city_car_management
   
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv

   # Para Linux/Mac
   source venv/bin/activate  
   
   # Para Windows
   venv\Scripts\activate    
   
3. Instale as dependências (se não estiver usando Docker):
   ```bash
   pip install -r requirements.txt

## Configuração do Docker

1. Construa e inicie os containers (lembre-se de criar um .env):
   ```bash
   docker-compose --env-file .env up -d --build
   
2. Acesse o aplicativo em seu navegador:
- `http://localhost:5000`
- `http://localhost:5000/apidocs` (Swagger)

## Executando Migrações

1. Inicialize o diretório de migrações:
   ```bash
   docker-compose run web flask db init

2. Crie uma migração
   ```bash
   docker-compose run web flask db migrate -m "Initial migration"

3. Aplique as migrações ao banco de dados
   ```bash
   docker-compose run web flask db upgrade

## Executando Testes

1. Para rodar os testes, use o seguinte comando:
   ```bash
   docker-compose run test
