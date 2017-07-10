#!/usr/bin/env bash

docker rm -f backend
docker rm -f frontend

CC_BS="server 127.0.0.1:8080"
docker build -t "mrow4a/backend" Backend

#docker build --build-arg CC_BACKEND_SERVERS=${CC_BS} -t "mrow4a/frontend" Frontend
docker build --build-arg CC_BACKEND_SERVERS="server 127.0.0.1:8000 backup;" -t "mrow4a/frontend" Frontend

docker run --name backend -d -p 8000:80 mrow4a/backend:latest
docker run --name frontend -d -p 8080:80 mrow4a/frontend:latest

docker ps -a