# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
LABEL authors="marcelochsendorf"

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

EXPOSE 5500
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

CMD ["python3", "app.py"]


