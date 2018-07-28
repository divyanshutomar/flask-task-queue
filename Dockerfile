FROM python:3.6.5-alpine

RUN mkdir /usr/srv

WORKDIR /usr/srv

RUN apk add --update --no-cache libc-dev gcc libxslt-dev

RUN pip install pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --system

COPY . .

EXPOSE 5000

CMD ["honcho", "start"]
