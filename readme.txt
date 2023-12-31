#DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/gitusers"
in root folder:
uvicorn app.main:app --reload
uvicorn app.main:app --host 127.0.0.1 --port 5005 --reload

https://github.com/teamhide/fastapi-boilerplate/tree/master (fast api with async sqlalchemy)
docker build -t git-ranker-api .