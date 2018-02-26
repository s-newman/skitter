# Use the official python image for python 3.5 - using Alpine because it's
# super small and also best practices I guess
FROM python:3.5-alpine

# Create running directory
WORKDIR /api

# Copy over application files
COPY run.py ./run.py
COPY app ./app
COPY requirements.txt ./requirements.txt

# Install pip requirements
RUN pip3 install -r requirements.txt

# Configure uWSGI
COPY app.ini ./app.ini

# Run the application on startup
CMD uwsgi --ini app.ini
