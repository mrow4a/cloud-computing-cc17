[[TODO]]
FROM nginx:latest
MAINTAINER group32
RUN ./fix-nginx-conf.sh && sudo systemctl start nginx 
CMD
EXPOSE 80
ADD nginx.conf /etc/nginx/nginx.conf
COPY fix-nginx-conf.sh ./
VOLUME /hypervisor_etc