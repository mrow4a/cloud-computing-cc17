FROM nginx:latest
MAINTAINER group32

ENV CC_BACKEND_SERVERS="DEFAULT"

# https://docs.docker.com/engine/reference/builder/#add
ADD nginx.conf /etc/nginx/nginx.conf
ADD fix-nginx-conf.sh /

# This will run when starting the docker, gets overwriten by ENTRYPOINT if used
RUN chmod +x /fix-nginx-conf.sh

# Expose port 80 - https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80

CMD ./fix-nginx-conf.sh "${CC_BACKEND_SERVERS}" ; service nginx restart