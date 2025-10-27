# syntax=docker/dockerfile:1.6

FROM node:20-alpine AS base

WORKDIR /app

COPY ./package.json ./package-lock.json ./

RUN npm ci --omit=dev

COPY ./src ./src
COPY ./recipes.json ./static/

ENV NODE_ENV=production
ENV STATIC_RECIPES=/app/static

EXPOSE 4000

CMD ["node", "src/server.js"]
