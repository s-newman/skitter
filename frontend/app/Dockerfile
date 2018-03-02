# Based on the official ubuntu image
FROM ubuntu

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev \
    python3-pip

# Copy over application files
COPY run.py /var/www/run.py
COPY ui /var/www/ui
COPY requirements.txt /var/www/requirements.txt

# Set the working directory to app root (right above ui/)
WORKDIR /var/www/

# Install requirements and update pip
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip

# Configure uWSGI
COPY ui.ini /var/www/ui.ini

# Expose port 80 for running webserver
EXPOSE 80
