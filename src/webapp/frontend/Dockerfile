# syntax=docker/dockerfile:1.4
FROM node:alpine
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN rm -rf node_modules
RUN npm install
RUN npm run build
EXPOSE 3000
CMD ["npm", "run" ,"serve"]