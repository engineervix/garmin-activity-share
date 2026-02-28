FROM python:3.13-slim-bullseye

# Add user that will be used in the container
RUN groupadd tweepy && \
    useradd --create-home --shell /bin/bash -g tweepy tweepy

RUN mkdir -p /home/tweepy/app && chown tweepy:tweepy /home/tweepy/app

# set work directory
WORKDIR /home/tweepy/app

# set environment variables
# - Force Python stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH=/home/tweepy/app

# Set timezone to Africa/Lusaka
RUN ln -fs /usr/share/zoneinfo/Africa/Lusaka /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

# Install system dependencies required by the project
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Use user "tweepy" to run the build commands below and the server itself.
USER tweepy

# MODE is either `dev` or `production`
ARG MODE
ENV MODE ${MODE}

# install python dependencies
ENV VIRTUAL_ENV=/home/tweepy/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install pip-tools
COPY --chown=tweepy requirements requirements
COPY --chown=tweepy ./requirements.txt .
COPY --chown=tweepy ./requirements-dev.txt .
RUN pip-compile requirements/${MODE}.in --output-file requirements/${MODE}.txt
RUN if [ "$MODE" = "dev" ]; then pip-sync requirements-${MODE}.txt; else pip-sync requirements.txt; fi

# Copy the source code of the project into the container
COPY --chown=tweepy:tweepy . .

# Runtime command that executes when "docker run" is called
# basically, do nothing ... we'll run commands ourselves
CMD tail -f /dev/null
