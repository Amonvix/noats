from bs4 import BeautifulSoup
import re
from langdetect import detect
import logging

logger = logging.getLogger(__name__)


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


def detectar_idioma(texto: str) -> str:
    """
    Detecta o idioma de um texto e retorna 'pt' para português
    ou 'en' para inglês. Fallback para 'pt' se não identificado.
    """
    try:
        lang = detect(texto)
        if lang.startswith('pt'):
            return 'pt'
        elif lang.startswith('en'):
            return 'en'
        else:
            logger.warning(
                f"Idioma desconhecido detectado: {lang}, fallback para 'pt'")
            return 'pt'
    except Exception as e:
        logger.error(f"Erro ao detectar idioma: {e}, fallback para 'pt'")
        return 'pt'
