FROM python:3.8.2-alpine

ARG FLASK_ENV
ENV FLASK_ENV=$FLASK_ENV
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && apk add bash
RUN apk add py2-pip autoconf automake g++ make --no-cache
RUN apk add libffi-dev

RUN pip install py-bcrypt
RUN pip install psycopg2-binary
RUN apk del build-deps

RUN pip install pipenv

COPY . ./

RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD ["gunicorn", "flask_app:app"]
