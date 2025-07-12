from bs4 import BeautifulSoup
import re


def extrair_texto_bruto(html: str) -> str:
    """Extracts raw visible text from HTML"""
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts, styles, etc.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    texto = soup.get_text(separator=' ')
    return texto


def limpar_texto(texto: str) -> str:
    """Cleans up raw text, removing excess spaces and artifacts"""
    texto = re.sub(r"\s+", " ", texto)  # multiple spaces -> one
    texto = texto.strip()
    return texto


def detectar_pcd(texto: str) -> bool:
    """Detect if the job description mentions affirmative action for PCD"""
    padroes_pcd = [
        r"\bpcd\b",
        r"pessoa com deficiência",
        r"inclusão",
        r"cotas?",
        r"vaga afirmativa",
        r"diversidade"
    ]

    for padrao in padroes_pcd:
        if re.search(padrao, texto, re.IGNORECASE):
            return True

    return False
