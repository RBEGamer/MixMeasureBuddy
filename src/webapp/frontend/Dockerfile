# syntax=docker/dockerfile:1.6

FROM node:20-alpine AS builder

WORKDIR /app/frontend

COPY ./package.json ./
COPY ./package-lock.json ./

RUN npm ci

COPY ./ ./

RUN npm run build

FROM nginx:1.27-alpine AS runner

COPY --from=builder /app/frontend/out /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
