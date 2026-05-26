import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def buscar_personagem(character):
    character = character.lower()
    caminho = f"personagens/{character}.json"

    if os.path.exists(caminho):# Carrega o arquivo
        with open(caminho, encoding="utf-8") as f:
            ficha = json.load(f)
            return ficha # Abre a ficha
    else:
        for arquivo in os.listdir("personagens"): # Verifica todos os arquvos da pasta
            with open(f"personagens/{arquivo}", encoding = "utf-8") as f: # Carrega o arquivo
                ficha = json.load(f)
                return ficha # Se existir, abre a ficha
        return None # Se não tiver o nome em nenhum arquiva, retorna none

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