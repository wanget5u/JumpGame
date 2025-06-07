FROM python:3.11-slim

WORKDIR /app

COPY . /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pygame \
    libgl1-mesa-glx \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    fontconfig \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]