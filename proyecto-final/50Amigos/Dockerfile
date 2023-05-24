# pull official base image
FROM python:3.9.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TERM xterm-256color
ENV LIBRARY_PATH=/lib:/usr/lib

# install psycopg2 dependencies
RUN apk update && apk upgrade \
    && apk add postgresql-dev gcc python3-dev musl-dev bash \
    jpeg-dev zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# To collect static properly
RUN adduser -D user
USER user

# run entrypoint.sh
ENTRYPOINT ["bash", "-c", "/usr/src/app/entrypoint.sh"]
