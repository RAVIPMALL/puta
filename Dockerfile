FROM python:3.10-alpine3.13
LABEL maintainer="rp"

ENV PYTHONBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN apk add --no-cache --virtual .build-deps \
        gcc musl-dev python3-dev libffi-dev jpeg-dev zlib-dev \
        freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && apk del .build-deps

ENV PATH="/py/bin:$PATH"