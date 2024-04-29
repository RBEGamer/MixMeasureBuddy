FROM ubuntu:22.04

RUN apt update && apt upgrade -y



RUN apt install -y apache2 curl wget

EXPOSE 80

RUN sed -i '1s/^/ServerName mixmeasurebuddy_webapp\n/' /etc/apache2/apache2.conf

RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod proxy_balancer
RUN a2enmod lbmethod_byrequests
RUN a2enmod rewrite

CMD ["apache2ctl", "-D", "FOREGROUND"]