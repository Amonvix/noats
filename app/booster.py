import re
from collections import Counter


def extrair_palavras_chave(texto_vaga: str, top_n: int = 10):
    """Extrai as palavras mais frequentes da vaga, ignorando stopwords básicas"""
    stopwords = {'e', 'em', 'de', 'para', 'com', 'a', 'o', 'os',
                 'as', 'um', 'uma', 'por', 'na', 'no', 'nas', 'nos'}
    palavras = re.findall(r'\b\w+\b', texto_vaga.lower())
    palavras_filtradas = [p for p in palavras if len(
        p) > 2 and p not in stopwords]
    contagem = Counter(palavras_filtradas)
    mais_comuns = [palavra for palavra, _ in contagem.most_common(top_n)]
    return mais_comuns


def reforcar_hardskills(hard_skills: list, palavras_chave: list):
    """Adiciona palavras-chave relevantes às hard skills, sem duplicar"""
    for palavra in palavras_chave:
        if palavra.capitalize() not in hard_skills:
            hard_skills.append(palavra.capitalize())
    return hard_skills
