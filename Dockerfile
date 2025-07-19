# Imagem base oficial leve
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Instala libs do sistema para WeasyPrint + dependências Python
RUN apt-get update && apt-get install -y \
build-essential \
libpango-1.0-0 \
libpangoft2-1.0-0 \
libpangocairo-1.0-0 \
libcairo2 \
libgdk-pixbuf2.0-0 \
libffi-dev \
fonts-liberation \
&& rm -rf /var/lib/apt/lists/*

# Copia dependências primeiro (pra cache funcionar)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta padrão do Uvicorn
EXPOSE 8080

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

