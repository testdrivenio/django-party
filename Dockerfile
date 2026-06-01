###########
# BUILDER #
###########

# pull official base image
FROM python:3.14-slim-bookworm AS builder

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# install system dependencies
RUN apt-get update \
  && apt-get -y install ca-certificates curl gnupg \
  && apt-get clean

# install node
ENV NODE_MAJOR=24
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install nodejs -y

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# export production dependencies and install them
COPY pyproject.toml uv.lock ./
RUN uv export --no-hashes --no-dev > requirements.txt \
  && uv pip install --system --no-cache -r requirements.txt

# install Node.js dependencies
COPY package.json package-lock.json ./
RUN npm install

# build Tailwind and collect static files
COPY . .
RUN npm run tailwind:build && python manage.py collectstatic --noinput

#########
# FINAL #
#########

# pull official base image
FROM python:3.14-slim-bookworm

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

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
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=prod
ENV TESTING=0
ENV PYTHONPATH=$APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/requirements.txt .
COPY --from=builder /usr/src/app/staticfiles $APP_HOME/staticfiles
RUN uv pip install --system --no-cache -r requirements.txt

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $HOME
# change to the app user
USER app
# serve the application
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
