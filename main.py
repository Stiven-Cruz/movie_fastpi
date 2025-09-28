from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from db.database import engine, Base
from routers.movie import router_movie
from routers.users import login_user

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Primeros pasos de una API",
    version="0.0.6"
)

app.include_router(router_movie)
app.include_router(login_user)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["inicio"])
def read_root():
    return HTMLResponse("<h1>Hola Mundo!</h1>")