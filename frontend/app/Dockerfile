# Based on the official ubuntu image
FROM ubuntu

# Set the working directory to app root (right above ui/)
WORKDIR /var/www/

# Expose port 80 for running webserver
EXPOSE 80

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    libmysqlclient-dev

# Install requirements and update pip
COPY requirements.txt /var/www/requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip

# Install mysql connector
RUN wget https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python_2.1.7-1ubuntu14.04_all.deb
RUN sudo dpkg -i mysql-connector-python_2.1.7-1ubuntu14.04_all.deb

# Configure uWSGI
COPY ui.ini /var/www/ui.ini

# Copy over application files
COPY run.py /var/www/run.py
COPY ui /var/www/ui
