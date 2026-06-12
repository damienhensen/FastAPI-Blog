# FastAPI Blog API

A simple blog backend built with FastAPI.

The goal of this project is to learn Python and FastAPI by building a real REST API.

## Requirements

- Python 3.x
- Docker
- Docker Compose

## Setup

### Create a virtual environment:

```bash
python -m venv .venv
```

### Activate it:

#### Linux/macOS

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Create .env file:

```bash
cp .env.example .env
```

### Start docker containers:

```bash
docker compose up -d
```

### Run migrations:

```bash
alembic upgrade head
```

### Run the application:

```bash
fastapi dev
```

#### The API will be available at:

http://localhost:8000

#### Swagger documentation:

http://localhost:8000/docs