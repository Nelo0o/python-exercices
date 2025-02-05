from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.models import init_db
import routes
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Jeu de cartes",
    description="API avec base de données SQLite pour gérer un jeu de cartes.",
    version="1.0.0",
    lifespan=lifespan
)

# Routes
app.post("/paquet")(routes.creer_paquet)
app.get("/paquets")(routes.liste_paquets)
app.get("/paquet/{paquet_id}")(routes.get_paquet)
app.get("/paquet/{paquet_id}/distribuer/{nb_joueurs}")(routes.distribuer_cartes)
app.get("/paquet/{paquet_id}/mains")(routes.voir_mains)
app.post("/paquet/{paquet_id}/melanger")(routes.melanger_paquet)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
