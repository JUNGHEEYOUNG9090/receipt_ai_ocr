FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3.11 -m pip install --upgrade pip
RUN python3.11 -m pip install -r requirements.txt

RUN python3.11 -m pip install paddlepaddle-gpu==3.3.1 \
    -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

COPY app ./app

EXPOSE 8000

CMD ["python3.11", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]