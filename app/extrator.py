import pdfplumber


def extrair_dados_curriculo(caminho_arquivo: str) -> dict:
    texto = extrair_texto_pdf(caminho_arquivo)
    candidato = {
        "nome": "Detectado",
        "cargo": "Detectado",
        "email": "Detectado",
        "telefone": "Detectado",
        "linkedin": "Detectado",
        "github": "Detectado",
        "resumo_profissional": "Detectado",
        "experiencias": [],
        "formacoes": [],
        "hard_skills": [],
        "soft_skills": [],
        "idiomas": []
    }
    # aqui você implementa as heurísticas pra preencher os campos
    return candidato


def extrair_texto_pdf(caminho_arquivo: str) -> str:
    texto = ""
    with pdfplumber.open(caminho_arquivo) as pdf:
        for page in pdf.pages:
            texto += page.extract_text() + "\n"
    return texto
