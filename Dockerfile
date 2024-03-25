FROM python:3.12-slim

LABEL org.opencontainers.image.authors="Yuriy Novostavskiy" \
      org.opencontainers.image.source="" \
      org.opencontainers.image.license="MIT" \
      org.opencontainers.image.description="A simple bot that sends the update of alarms and exlosions"

RUN python -m pip install requests~=2.31.0 python-dotenv~=1.0.1

WORKDIR /bot

COPY bot/* ./

ENTRYPOINT [ "python", "main.py" ]