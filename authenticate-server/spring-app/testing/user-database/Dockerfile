# Based on the official MySQL 5.7 Docker image
FROM mysql:5.7

# Change passwords
#ENV MYSQL_RANDOM_ROOT_PASSWORD="yes"
#ENV MYSQL_USER="api-gateway"
#ENV MYSQL_PASSWORD="changemeplease-securitysucks"
ENV MYSQL_ALLOW_EMPTY_PASSWORD="yes"

# Create the database
COPY database.sql /docker-entrypoint-initdb.d/database.sql
ENV MYSQL_DATABASE="users"
