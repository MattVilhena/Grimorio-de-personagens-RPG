import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return RedirectResponse(url="/frontend/index.html")

def buscar_personagem(character):
    character = character.lower().strip()
    for arquivo in os.listdir("personagens"):
        if arquivo.endswith(".json"):
            nome_arquivo_limpo = arquivo.replace(".json", "").lower()
            if nome_arquivo_limpo in character:
                caminho = f"personagens/{arquivo}"
                with open(caminho, encoding="utf-8") as f:
                    ficha = json.load(f)
                    return ficha
    return None

@app.get("/personagem/{character}")
def get_personagem(character: str):
    ficha = buscar_personagem(character)

    if ficha is None:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return ficha

@app.get("/personagens")
def listar_personagens():
    names = []
    for arquivo in os.listdir("personagens"):
        if arquivo.endswith(".json"):
            name = arquivo.replace(".json", "")
            names.append(name)
    return names
