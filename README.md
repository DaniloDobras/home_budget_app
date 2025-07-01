# home_budget_app

This is the simple application for home budget monitoring

## 🚀 Quick Start

**Clone the repository**
```bash
git clone https://github.com/DaniloDobras/home_budget_app.git
cd home_budget_app
```

Install python 3.11 using pyenv or manually

Install Docker desktop:
- MacOS: https://docs.docker.com/desktop/setup/install/mac-install/
- Windows: https://docs.docker.com/desktop/setup/install/windows-install/

**Run docker compose**
```bash
docker-compose up --build
```

**Visit the docs**  

home_budget_app/openapi.json

or

```code
http://0.0.0.0:8000/docs
```

Need to have a well-configured .env file. Please see home_budget_app/env.example.

## Local Setup

```bash
pip install -r requirements.txt
```

**Database setup**  

- It is necessary to have a properly configured database server
- PostgreSQL https://www.postgresql.org/download/  
- It is necessary to have a properly filled .env file with credentials to the database

After db is configured, migrations should be executed:
```bash
alembic upgrade head
```

Now, server running:  

```bash
uvicorn app.main:app --reload
```

Please try to ping:  

```code
http://127.0.0.1:8000/docs
```
