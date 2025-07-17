📄 Gerador Inteligente de Currículo
Um app web leve e responsivo para gerar currículos inteligentes otimizados para aumentar as chances de um candidato ser selecionado para entrevista.
A ideia não é burlar sistemas ATS, mas organizar as informações do candidato de forma estratégica, clara e adaptada à vaga desejada.

🚀 Como funciona?
✅ Você fornece:

A URL da vaga ou o texto completo da vaga.

Um arquivo PDF com seu currículo base.

O idioma desejado para o currículo (Português ou Inglês).

✅ O sistema:

Analisa os requisitos da vaga.

Ajusta as hard skills do currículo para destacar as mais relevantes.

Gera um PDF bem formatado, pronto para ser enviado.

🌐 Deploy rápido no Fly.io
Este projeto já foi pensado para rodar leve em ambientes como o Fly.io.

Pré-requisitos:
Conta no Fly.io

Fly CLI instalado

Rodando localmente:
bash
Copiar
Editar
docker build -t gerador-curriculo .
docker run -p 8000:8000 gerador-curriculo
Acesse em http://localhost:8000

Subindo no Fly:
bash
Copiar
Editar
fly launch
fly deploy
🧾 Tecnologias usadas
Python 3.10

FastAPI

Uvicorn

WeasyPrint

Jinja2

Docker

🎯 Objetivo
Este projeto foi criado para maximizar a possibilidade do candidato ser notado e convidado para uma conversa, apresentando suas competências alinhadas à vaga pretendida, sem práticas enganosas ou de manipulação indevida.