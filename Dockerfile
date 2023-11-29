###########
# BUILDER #
###########

# pull official base image
FROM python:3.12-slim-bookworm as builder

# install system dependencies
RUN apt-get update \
  && apt-get -y install g++ ca-certificates curl gnupg \
  && apt-get clean

# install node
ENV NODE_MAJOR=20
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install nodejs -y

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY . .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# Build Tailwind
RUN pip install -r requirements.txt && python manage.py tailwind install && python manage.py tailwind build && python manage.py collectstatic --noinput

#########
# FINAL #
#########

# pull official base image
FROM python:3.12-slim-bookworm

# upgrade system packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0
ENV PYTHONPATH $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
COPY --from=builder /usr/src/app/staticfiles $APP_HOME/staticfiles
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $HOME
# change to the app user
USER app
# serve the application
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
