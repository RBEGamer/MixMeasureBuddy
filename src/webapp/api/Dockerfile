# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine
LABEL authors="marcelochsendorf"

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 5500


CMD ["python3", "app.py"]


