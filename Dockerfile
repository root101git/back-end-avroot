FROM python:3.11.3-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    apt-utils \
    curl \
    wget \
    git \
    libgl1 \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /backend

COPY . /backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "uvicorn","main:app","--reload","--host","0.0.0.0","--port","8080" ]
