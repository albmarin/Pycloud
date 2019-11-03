FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ARG BACKEND_ENV=production
ARG APP_MODULE="pycloud_api.main:app"

ENV ENV=${BACKEND_ENV}
ENV APP_MODULE=${APP_MODULE}

COPY . /app
WORKDIR /app

RUN apt update; apt install dos2unix
RUN find /app -type f -print0 | xargs -0 dos2unix
RUN sh ./prestart.sh
