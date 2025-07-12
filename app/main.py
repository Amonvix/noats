import json
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

with open("dados_candidato.json") as f:
    candidato = json.load(f)

class VagaRequest(BaseModel):
    url: str

@app.post("/processar-url")
def processar_url(vaga: VagaRequest):
    resp = requests.get(vaga.url)
    soup = BeautifulSoup(resp.text, "html.parser")
    texto = soup.get_text()

    # Verificar se é vaga afirmativa PCD
    if any(palavra in texto.lower() for palavra in ["pcd", "pessoa com deficiência", "inclusão"]):
        template = "PCD"
    else:
        template = "STANDARD"

    return {
        "preview": texto[:1000],
        "template": template,
        "dados_candidato": candidato
    }  # retorna um preview pra não explodir
