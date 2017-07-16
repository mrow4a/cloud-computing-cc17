FROM nginx:latest
MAINTAINER group32

# https://docs.docker.com/engine/reference/builder/#volume
VOLUME /hypervisor_etc

# Define default env variable which should be passed to frontend docker
ENV CC_BACKEND_SERVERS="DEFAULT"

# https://docs.docker.com/engine/reference/builder/#add
ADD nginx.conf /etc/nginx/nginx.conf
ADD fix-nginx-conf.sh /

# This will run when building the docker
RUN apt-get update && apt-get install -y curl && chmod +x /fix-nginx-conf.sh

# Expose port 80 - https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80

CMD ./fix-nginx-conf.sh "${CC_BACKEND_SERVERS}" ; nginx