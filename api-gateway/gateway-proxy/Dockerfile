# Based on the official nginx image
FROM nginx

# Copy over nginx configuration files
COPY nginx.conf /etc/nginx/nginx.conf

# Remove default configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Expose port 80 for running webserver
EXPOSE 80
