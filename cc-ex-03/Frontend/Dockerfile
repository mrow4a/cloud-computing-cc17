FROM nginx:latest
MAINTAINER group32

ARG CC_BACKEND_SERVERS

# https://docs.docker.com/engine/reference/builder/#add
ADD nginx.conf /etc/nginx/nginx.conf
ADD fix-nginx-conf.sh /

# This will run when starting the docker, gets overwriten by ENTRYPOINT if used
RUN chmod +x /fix-nginx-conf.sh && ./fix-nginx-conf.sh '${CC_BACKEND_SERVERS}'

# Expose port 80 - https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80

# https://docs.docker.com/engine/reference/builder/#volume
VOLUME /hypervisor_etc

CMD service nginx restart