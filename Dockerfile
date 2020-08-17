FROM python:3.8.2-alpine

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && apk add bash

RUN pip install psycopg2-binary
RUN apk del build-deps

RUN pip install pipenv

COPY . ./

RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]
