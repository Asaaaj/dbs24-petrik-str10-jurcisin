from fastapi import FastAPI
from dbs_assignment_jurcisin.router import router

app = FastAPI(title="DBS")
app.include_router(router)

#docker run -p 127.0.0.1:8000:8000 --env DATABASE_HOST=host.docker.internal --env DATABASE_PORT=5432 --env DATABASE_NAME=postgres --env DATABASE_USER=postgres --env DATABASE_PASSWORD=7355608 --name dbs24-petrik-str10-jurcisin-container dbs24-petrik-str10-jurcisin