#!/bin/bash
clear
#docker compose build --no-cache
docker compose build #--no-cache

docker compose down -v

docker compose up -d
