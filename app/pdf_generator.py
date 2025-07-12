import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def gerar_pdf_jinja(dados_candidato: dict, template_nome: str, caminho_arquivo: str):
    """Gera PDF usando um template HTML e dados dinâmicos"""
    template_html = env.get_template(template_nome)

    # monta contexto
    contexto = {
        "nome": dados_candidato.get("nome", ""),
        "cargo": dados_candidato.get("cargo", ""),
        "email": dados_candidato.get("email", ""),
        "telefone": dados_candidato.get("telefone", ""),
        "linkedin": dados_candidato.get("linkedin", ""),
        "github": dados_candidato.get("github", ""),
        "resumo_profissional": dados_candidato.get("resumo_profissional", ""),
        "experiencias": dados_candidato.get("experiencias", []),
        "formacoes": dados_candidato.get("formacoes", []),
        "hard_skills": dados_candidato.get("hard_skills", []),
        "soft_skills": dados_candidato.get("soft_skills", []),
        "idiomas": dados_candidato.get("idiomas", []),
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    html_renderizado = template_html.render(contexto)

    HTML(string=html_renderizado).write_pdf(caminho_arquivo)
