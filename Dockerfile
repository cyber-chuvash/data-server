FROM python:3.7-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
RUN apk update && apk add --no-cache --virtual .build-deps libffi libffi-dev musl musl-dev gcc python3-dev postgresql-dev

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --prefix /install -r /requirements.txt


FROM base
RUN apk update && apk add --no-cache libpq
COPY --from=builder /install /usr/local
COPY server/ /app/server/
COPY app.py /app/
WORKDIR /app

EXPOSE 80
CMD python3 app.py -H 0.0.0.0 -P 80
