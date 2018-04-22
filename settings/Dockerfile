FROM php:7-apache

RUN docker-php-ext-install mysqli
RUN docker-php-ext-enable mysqli

COPY src/ /var/www/html/
COPY img/ /var/www/html/