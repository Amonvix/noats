import json
import os
import shutil

import requests
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from langdetect import detect

from . import ats_booster, parser, pdf_generator
from .logger import logger

TMP_DIR = "tmp"
os.makedirs(TMP_DIR, exist_ok=True)

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def form_html():
    logger.info("Página inicial acessada")
    return """
    <html>
        <head>
            <title>Gerador de Currículo</title>
        </head>
        <body>
            <h1>Gerador Inteligente de Currículo</h1>
            <form action="/gerar" enctype="multipart/form-data" method="post">
                <label>URL da vaga:</label><br>
                <input type="text" name="vaga_url" style="width:400px"/><br><br>
                <label>Upload do currículo base (PDF):</label><br>
                <input type="file" name="curriculo_pdf"/><br><br>
                <button type="submit">Gerar Currículo</button>
            </form>
        </body>
    </html>
    """


@app.post("/gerar")
async def gerar_curriculo(vaga_url: str = Form(...), curriculo_pdf: UploadFile = File(...)):
    try:
        logger.info(
            f"Requisição recebida: URL={vaga_url}, Currículo={curriculo_pdf.filename}")

        # Salva PDF base temporário
        pdf_base_path = os.path.join(TMP_DIR, curriculo_pdf.filename)
        with open(pdf_base_path, "wb") as buffer:
            shutil.copyfileobj(curriculo_pdf.file, buffer)

        # Scraping da vaga
        resp = requests.get(vaga_url)
        resp.raise_for_status()
        html = resp.text
        logger.info(f"Scraping bem-sucedido da vaga: {vaga_url}")

        texto_bruto = parser.extrair_texto_bruto(html)
        texto_limpo = parser.limpar_texto(texto_bruto)

        # Detecta idioma
        idioma = parser.detectar_idioma(texto_limpo)
        logger.info(f"Idioma detectado: {idioma}")

        # Carrega candidato no idioma certo
        json_path = f"dados_candidato_{idioma}.json"
        with open(json_path) as f:
            candidato = json.load(f)

        # Detecta PCD
        is_pcd = parser.detectar_pcd(texto_limpo)
        logger.info(f"Detecção PCD: {'Sim' if is_pcd else 'Não'}")

        # Define template lógico
        template_nome = f"{'PCD' if is_pcd else 'STANDARD'}_{idioma.upper()}"

        # Palavras-chave da vaga
        palavras_chave = ats_booster.extrair_palavras_chave(
            texto_limpo, idioma=idioma)
        candidato['hard_skills'] = ats_booster.reforcar_hardskills(
            candidato.get('hard_skills', []), palavras_chave)

        # Insere URL da vaga no contexto
        candidato['vaga_url'] = vaga_url

        # Nome do PDF final
        pdf_final_path = os.path.join(
            TMP_DIR, f"curriculo_gerado_{template_nome}.pdf")

        # Gera PDF
        pdf_generator.gerar_pdf_jinja(
            dados_candidato=candidato,
            template_nome='model.html',
            caminho_arquivo=pdf_final_path
        )

        os.remove(pdf_base_path)

        logger.info(f"PDF gerado com sucesso: {pdf_final_path}")
        return FileResponse(pdf_final_path, filename=f"Curriculo_Gerado_{template_nome}.pdf", media_type='application/pdf')

    except Exception as e:
        logger.error(f"Erro inesperado no processamento: {e}")
        raise
