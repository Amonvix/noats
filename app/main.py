from fastapi.responses import JSONResponse
from . import parser
import json
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from . import pdf_generator

app = FastAPI()

with open("dados_candidato.json") as f:
    candidato = json.load(f)


class VagaRequest(BaseModel):
    url: str


@app.post("/processar-url")
def processar_url(vaga: VagaRequest):
    # Faz o request da página
    resp = requests.get(vaga.url)
    html = resp.text

    # Processa com o parser
    texto_bruto = parser.extrair_texto_bruto(html)
    texto_limpo = parser.limpar_texto(texto_bruto)

    # Detecta PCD
    is_pcd = parser.detectar_pcd(texto_limpo)

    # define idioma
    idioma = candidato.get("idioma", "pt")  # default pt

    # Define template

    template = f"PCD_{idioma.upper()}" if is_pcd else f"STANDARD_{idioma.upper()}"

    arquivo_pdf = f"curriculo_gerado_{template}.pdf"
    # Gera PDF
    pdf_generator.gerar_pdf(
        dados_candidato=candidato,
        texto_vaga=texto_limpo,
        template=template,
        caminho_arquivo=arquivo_pdf
    )

    # Retorna resposta
    return JSONResponse({
        "mensagem": "Currículo gerado com sucesso",
        "arquivo": arquivo_pdf,
        "template": template
    })
