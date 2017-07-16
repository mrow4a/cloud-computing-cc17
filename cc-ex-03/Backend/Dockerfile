FROM nginx:latest
MAINTAINER group32

# https://docs.docker.com/engine/reference/builder/#volume
VOLUME /hypervisor_etc

# https://docs.docker.com/engine/reference/builder/#add
ADD nginx.conf /etc/nginx/nginx.conf
ADD fix-nginx-conf.sh /

# This will run when starting the docker
RUN apt-get update && apt-get install -y curl && chmod +x /fix-nginx-conf.sh

# Expose port 80 - https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80

CMD ./fix-nginx-conf.sh ; nginx