# Use the official python image for python 3.5 - using Alpine because it's
# super small and also best practices I guess
FROM python:3.5-alpine

# Create running directory
RUN mkdir /api

# Copy over application files
COPY run.py /api/run.py
COPY app /api/app
COPY requirements.txt /api/requirements.txt

# Install pip requirements
RUN pip3 install -r requirements.txt

# Configure uWSGI
COPY app.ini /app/app.ini

# Run the application on startup
CMD uwsgi --ini app.ini
