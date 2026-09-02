FROM node:22-bookworm-slim AS provider-builder

WORKDIR /provider

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git .

WORKDIR /provider/server

RUN npm ci
RUN npx tsc


FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY --from=provider-builder /usr/local/bin/node /usr/local/bin/node
COPY --from=provider-builder /usr/local/lib/node_modules /usr/local/lib/node_modules

COPY --from=provider-builder /provider /opt/bgutil-ytdlp-pot-provider

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p downloads

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]