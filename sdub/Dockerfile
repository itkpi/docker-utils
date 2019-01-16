FROM python:3.7.2-alpine3.8

RUN pip install jinja2

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python", "sdub.py" ]
