import json
import os
import shutil

import requests
from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-color: #282a36;
            color: #f8f8f2;
            font-family: Arial, sans-serif;
            font-size: 22px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 10px;
        }
        .container {
            background-color: #44475a;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px #6272a4;
            width: 100%;
            max-width: 600px;
        }
        h1 {
            text-align: center;
            color: #bd93f9;
            font-size: 26px;
        }
        label {
            display: block;
            margin-top: 15px;
            color: #f8f8f2;
            font-size: 20px;
        }
        input[type=text],
        input[type=file],
        textarea {
            width: 100%;
            padding: 10px;
            font-size: 18px;
            margin-top: 5px;
            border: none;
            border-radius: 4px;
            box-sizing: border-box;
        }
        textarea {
            resize: vertical;
        }
        button {
            margin-top: 20px;
            width: 100%;
            padding: 12px;
            font-size: 20px;
            background-color: #50fa7b;
            color: #282a36;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #8be9fd;
        }
        .radio-group {
            margin-top: 10px;
        }
        @media (max-width: 600px) {
            body {
                font-size: 18px;
            }
            h1 {
                font-size: 22px;
            }
            .container {
                padding: 15px;
            }
            label {
                font-size: 18px;
            }
            button {
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Gerador Inteligente de Currículo</h1>
        <form action="/gerar" enctype="multipart/form-data" method="post">
            <label>URL da vaga:</label>
            <input type="text" name="vaga_url"/>

            <label>Ou cole o conteúdo da vaga aqui (até 10.000 caracteres):</label>
            <textarea name="vaga_texto" rows="10" maxlength="10000"></textarea>

            <label>Upload do currículo base (PDF):</label>
            <input type="file" name="curriculo_pdf" required/>

            <label>Idioma desejado:</label>
            <div class="radio-group">
                <input type="radio" name="idioma" value="pt" checked/> Português
                <input type="radio" name="idioma" value="en"/> English
            </div>

            <button type="submit">Gerar Currículo</button>
        </form>
    </div>
</body>
</html>
    """


@app.post("/gerar")
async def gerar_curriculo(
    vaga_url: str = Form(""),
    vaga_texto: str = Form(""),
    curriculo_pdf: UploadFile = File(...),
    idioma_form: str = Form(None)
):
    try:
        logger.info(
            f"Requisição recebida: URL={vaga_url!r}, Texto colado={bool(vaga_texto)}, Currículo={curriculo_pdf.filename}, Idioma_form={idioma_form!r}"
        )

        # Garantir que o idioma foi informado
        if idioma_form not in ['pt', 'en']:
            logger.warning(
                "Idioma não informado pelo formulário, usando 'pt' como padrão.")
            idioma_form = 'pt'

        # Salva PDF base temporário
        pdf_base_path = os.path.join(TMP_DIR, curriculo_pdf.filename)
        with open(pdf_base_path, "wb") as buffer:
            shutil.copyfileobj(curriculo_pdf.file, buffer)

        # Pega texto da vaga
        if vaga_texto.strip():
            logger.info("Usando texto colado no formulário.")
            texto_limpo = parser.limpar_texto(vaga_texto)
        else:
            logger.info(f"Fazendo scraping da URL: {vaga_url}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
            resp = requests.get(vaga_url, headers=headers)
            resp.raise_for_status()
            html = resp.text
            texto_bruto = parser.extrair_texto_bruto(html)
            texto_limpo = parser.limpar_texto(texto_bruto)

        # Usa apenas idioma escolhido
        idioma = idioma_form
        logger.info(f"Idioma selecionado: {idioma}")

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
            texto_limpo, idioma=idioma
        )
        candidato['hard_skills'] = ats_booster.reforcar_hardskills(
            candidato.get('hard_skills', []), palavras_chave
        )

        # Insere URL da vaga no contexto, se tiver
        candidato['vaga_url'] = vaga_url

        # Nome do PDF final
        pdf_final_path = os.path.join(
            TMP_DIR, f"curriculo_gerado_{template_nome}.pdf"
        )

        # Gera PDF
        pdf_generator.gerar_pdf_jinja(
            dados_candidato=candidato,
            template_nome='model.html',
            caminho_arquivo=pdf_final_path
        )

        os.remove(pdf_base_path)

        logger.info(f"PDF gerado com sucesso: {pdf_final_path}")
        return FileResponse(
            pdf_final_path,
            filename=f"Curriculo_Gerado_{template_nome}.pdf",
            media_type='application/pdf'
        )

    except Exception as e:
        logger.error(f"Erro inesperado no processamento: {e}")
        raise
