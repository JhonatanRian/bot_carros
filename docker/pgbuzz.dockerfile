FROM postgres:13.1-alpine
LABEL maintainer "buzz <rodrigobentocoutinho@gmail.com>"
ENV POSTGRES_USER=buzz
ENV POSTGRES_PASSWORD=buzz_pass
ENV POSTGRES_DB=buzz_app
EXPOSE 5432
