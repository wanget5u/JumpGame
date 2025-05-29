FROM python:3.11

WORKDIR /app

# Zainstaluj zależności systemowe, w tym fontconfig
RUN apt-get update && apt-get install -y \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
