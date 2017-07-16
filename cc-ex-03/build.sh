#!/usr/bin/env bash

docker rm -f backend
docker rm -f frontend

export CC_BACKEND_SERVERS="172.17.0.1"
docker build -t "mrow4a/backend" Backend
docker run --name backend -d -p 8000:80 mrow4a/backend:latest

#docker build --build-arg CC_BACKEND_SERVERS=${CC_BS} -t "mrow4a/frontend" Frontend
docker build -t "mrow4a/frontend" Frontend
#docker run --name frontend --env CC_BACKEND_SERVERS=${CC_BACKEND_SERVERS} -v /etc:/hypervisor_etc -d -p 8080:80 mrow4a/frontend:latest
docker run --name frontend --env CC_BACKEND_SERVERS=$CC_BACKEND_SERVERS -v /etc:/hypervisor_etc -d -p 8080:80 mrow4a/frontend:latest
docker ps -a
curl localhost:8080
curl localhost:8080
curl localhost:8080

docker rm -f backend && \
docker push mrow4a/backend:latest && \
docker rm -f frontend && \
docker push mrow4a/frontend:latest && \
echo "Finished with success"