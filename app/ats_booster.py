import re
from collections import Counter

STOPWORDS_EN = {'and', 'you', 'join', 'ago', 'the', 'a', 'an', 'is', 'on',
                'in', 'to', 'for', 'with', 'by', 'of', 'at', 'or', 'as', 'sign', 'policy'}
STOPWORDS_PT = {'e', 'em', 'de', 'para', 'com', 'a', 'o',
                'os', 'as', 'um', 'uma', 'por', 'na', 'no', 'nas', 'nos'}


def extrair_palavras_chave(texto_vaga: str, idioma='pt', top_n: int = 10):
    stopwords = STOPWORDS_PT if idioma == 'pt' else STOPWORDS_EN
    palavras = re.findall(r'\\b\\w+\\b', texto_vaga.lower())
    palavras_filtradas = [p for p in palavras if len(
        p) > 2 and p not in stopwords]
    contagem = Counter(palavras_filtradas)
    mais_comuns = [palavra.capitalize()
                   for palavra, _ in contagem.most_common(top_n)]
    return mais_comuns


def reforcar_hardskills(hard_skills: list, palavras_chave: list):
    for palavra in palavras_chave:
        if palavra not in hard_skills:
            hard_skills.append(palavra)
    return hard_skills
