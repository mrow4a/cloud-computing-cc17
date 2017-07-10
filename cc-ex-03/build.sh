#!/usr/bin/env bash

docker rm -f backend

docker build -t "backend" Backend
docker build -t "frontend" Frontend

docker run --name backend -d -p 8080:80 backend:latest
docker run --name frontend -d -p 8080:80 frontend:latest

docker ps -a