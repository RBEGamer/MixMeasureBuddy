# syntax=docker/dockerfile:1.6

FROM node:20-alpine AS base

WORKDIR /app

RUN apk add --no-cache python3 make g++

COPY webapp/backend/package.json webapp/backend/package-lock.json ./
RUN npm ci --omit=dev

COPY webapp/backend/src ./src
COPY recipes ./static

ENV NODE_ENV=production
ENV STATIC_RECIPES=/app/static

EXPOSE 4000

CMD ["node", "src/server.js"]
