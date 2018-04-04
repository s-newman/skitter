# Based on the official MySQL 5.7 Docker image
FROM mysql:5.7

# Change passwords
#ENV MYSQL_RANDOM_ROOT_PASSWORD="yes"
ENV MYSQL_ROOT_PASSWORD = "bad"
ENV MYSQL_USER="api-gateway"
ENV MYSQL_PASSWORD="changemeplease-securitysucks"

COPY logging.cnf /etc/mysql/conf.d/logging.cnf

# Create the database
COPY database.sql /docker-entrypoint-initdb.d/database.sql
ENV MYSQL_DATABSE="users"
