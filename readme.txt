#DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/gitusers"
in root folder:
uvicorn app.main:app --reload
uvicorn app.main:app --host 127.0.0.1 --port 5005 --reload

https://github.com/teamhide/fastapi-boilerplate/tree/master (fast api with async sqlalchemy)
docker build -t git-ranker-api .
results from github scanner api:
"Name,Username,Url,Followers,Following,Forks,Commits,Stars,Code Lines,Tests,Keywords,Public Repos,Forked Repositories,Empty Repositories,Java Repositories,EJS Repositories,C# Repositories,JavaScript Repositories,Jupyter Notebook Repositories,C++ Repositories,CSS Repositories,Python Repositories,Node.js Repositories,Angular Repositories,React Repositories,HTML Repositories,Kotlin Repositories,C Repositories,TypeScript Repositories,Dart Repositories,Objective-C Repositories,Swift Repositories,Go Repositories,Rust Repositories,Ruby Repositories,Scala Repositories,PHP Repositories,R Repositories,SCSS Repositories,Assembly Repositories,Pawn Repositories\r\nNoam Rosenthal,noamr,https://github.com/noamr,102,4,34,386,132,17044,0,-,66,35,3,0,0,0,16,0,4,4,0,0,0,0,16,0,1,10,0,0,0,0,0,0,0,0,0,0,0,0\r\n"