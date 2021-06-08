FROM ubuntu

COPY . /app
WORKDIR /app

RUN set -ex \
    && apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    python3-venv \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*