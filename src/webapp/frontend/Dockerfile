# syntax=docker/dockerfile:1.6

FROM node:20-alpine AS builder

WORKDIR /app/frontend

COPY webapp/frontend/package.json webapp/frontend/package-lock.json ./

RUN npm ci

COPY webapp/frontend ./
COPY recipes /recipes

ARG NEXT_PUBLIC_BACKEND_URL=/api
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}

RUN npm run build

FROM nginx:1.27-alpine AS runner

COPY --from=builder /app/frontend/out /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
