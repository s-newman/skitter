FROM php:7-apache

RUN docker-php-ext-install mysqli
RUN docker-php-ext-enable mysqli

COPY img/ /var/www/html/img/
COPY src/ /var/www/html/