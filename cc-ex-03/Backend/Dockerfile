FROM nginx:latest
MAINTAINER group32

# This will run when starting the docker, gets overwriten by ENTRYPOINT if used
#CMD "./fix-nginx-conf.sh && sudo systemctl start nginx"
#CMD "sudo systemctl start nginx"

# Expose port 80 - https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 80

# https://docs.docker.com/engine/reference/builder/#add
#ADD nginx.conf /etc/nginx/nginx.conf
ADD fix-nginx-conf.sh ./

# https://docs.docker.com/engine/reference/builder/#volume
VOLUME /hypervisor_etc