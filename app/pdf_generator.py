from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def gerar_pdf(dados_candidato: dict, texto_vaga: str, template: str, caminho_arquivo: str):
    """Gera um PDF com base nos dados do candidato e análise da vaga"""
    c = canvas.Canvas(caminho_arquivo, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Currículo Gerado para Vaga")

    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    y -= 30
    c.drawString(50, y, f"Template selecionado: {template}")

    y -= 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Dados do Candidato:")

    y -= 20
    c.setFont("Helvetica", 12)
    for chave, valor in dados_candidato.items():
        c.drawString(60, y, f"{chave.capitalize()}: {valor}")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Descrição da Vaga:")

    y -= 20
    c.setFont("Helvetica", 10)
    texto_linhas = texto_vaga.split('\n')
    for linha in texto_linhas:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(60, y, linha.strip())
        y -= 12

    c.save()
