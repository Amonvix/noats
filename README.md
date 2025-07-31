#Acesse e teste o app gratis em: https://noats.fly.dev

# 📝 Gerador Inteligente de Currículo

Um app web **leve, responsivo e inteligente** para gerar currículos otimizados, aumentando suas chances de ser chamado para uma entrevista.

A ideia **não é burlar ATS**, mas organizar suas informações de forma estratégica, clara e adaptada à vaga desejada.

---

## 🚀 Como funciona?

✅ **Você fornece:**

* A **URL da vaga** ou o **texto completo da vaga** (copiado e colado).
* Um arquivo PDF com seu **currículo base**.
* O **idioma desejado** para o currículo (Português ou Inglês).

🤖 **O sistema:**

* Analisa os requisitos da vaga.
* Ajusta as **hard skills** do currículo para destacar as mais relevantes.
* Gera um PDF bem formatado e pronto para enviar.

---

## 🌎 Deploy rápido no Fly.io

Este projeto já foi planejado para rodar **leve** em ambientes como o [Fly.io](https://fly.io).

### Pré-requisitos:

* Conta no [Fly.io](https://fly.io)
* [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/) instalado

### Para rodar localmente:

```bash
docker build -t gerador-curriculo .
docker run -p 8000:8000 gerador-curriculo
```

Acesse: [http://localhost:8000](http://localhost:8000)

### Para subir no Fly.io:

```bash
fly launch
fly deploy
```

---

## 🛠️ Tecnologias utilizadas

* [Python 3.10](https://www.python.org)
* [FastAPI](https://fastapi.tiangolo.com)
* [WeasyPrint](https://weasyprint.org)
* [Jinja2](https://jinja.palletsprojects.com)
* [Uvicorn](https://www.uvicorn.org)
* [Docker](https://www.docker.com)

---

## 🎯 Objetivo

> Este projeto foi criado para **maximizar a possibilidade do candidato ser notado e convidado para uma conversa**, apresentando suas competências alinhadas à vaga pretendida, **sem práticas enganosas ou manipulação indevida**.

---
