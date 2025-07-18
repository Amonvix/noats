# Imagem base oficial leve
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia dependências primeiro (pra cache funcionar)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta padrão do Uvicorn
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

