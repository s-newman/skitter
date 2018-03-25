# Use the official python image for python 3.5 - using Alpine because it's
# super small and also best practices I guess
FROM python:3.5-alpine

# Create running directory
WORKDIR /api

# Install packages required to build uWSGI
RUN apk --update add build-base linux-headers

# Install pip requirements
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip

# Run the application on startup
CMD uwsgi --ini app.ini

# Configure uWSGI
COPY app.ini ./app.ini

# Copy over application files
COPY run.py ./run.py
COPY app ./app
