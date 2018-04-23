FROM openjdk:8

COPY ./spring-app /spring-app/

RUN cd /spring-app && ./gradlew bootJar

EXPOSE 8080

CMD java -jar /spring-app/build/libs/skitter-auth-0.0.1.jar
