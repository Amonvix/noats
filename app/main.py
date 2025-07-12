from fastapi.responses import JSONResponse
from . import parser
import json
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from . import pdf_generator
from . import ats_booster

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

    # Um pouco de Red Bull na confecção do personalizado
    palavras_chave = ats_booster.extrair_palavras_chave(texto_limpo)

    # reforça as hard skills com base na vaga
    candidato['hard_skills'] = ats_booster.reforcar_hardskills(
        candidato.get('hard_skills', []), palavras_chave)
    # Detecta PCD
    is_pcd = parser.detectar_pcd(texto_limpo)

    # Define idioma (default pt)
    idioma = candidato.get("idioma", "pt")

    # Define template
    if is_pcd:
        template = f"PCD_{idioma.upper()}"
    else:
        template = f"STANDARD_{idioma.upper()}"

    # Define nome do arquivo PDF
    arquivo_pdf = f"curriculo_gerado_{template}.pdf"

    # Gera PDF
    pdf_generator.gerar_pdf_jinja(
        dados_candidato=candidato,
        template_nome='model.html',
        caminho_arquivo=arquivo_pdf
    )

    # Retorna resposta
    return {
        "mensagem": "Currículo gerado com sucesso",
        "arquivo": arquivo_pdf,
        "template": template
    }
