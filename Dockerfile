FROM python:3.13.2

RUN apt-get update && apt-get install -y \
    python3-dev \
    libfreetype6-dev \
    libavformat-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt.txt

ENV DISPLAY=:0

CMD ["python", "main.py"]