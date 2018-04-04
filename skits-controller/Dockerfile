FROM node:8.11.0

COPY app/* /app/
COPY *.json /
COPY import.sh /

RUN npm install
RUN chmod +x /import.sh

EXPOSE 8080

CMD npm start