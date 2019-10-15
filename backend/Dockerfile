FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ARG BACKEND_ENV=production
ARG APP_MODULE="pycloud_api.main:app"

ENV ENV=${BACKEND_ENV}
ENV APP_MODULE=${APP_MODULE}

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
