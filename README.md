# Garmin Activity Share

> Fetch latest data from your Garmin Connect account and share (tweet) results

[![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![python3](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-brightgreen.svg)](https://python3statement.org/#sections50-why)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)

[![Build Status](https://github.com/engineervix/garmin-activity-share/actions/workflows/main.yml/badge.svg)](https://github.com/engineervix/garmin-activity-share/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/engineervix/garmin-activity-share/branch/main/graph/badge.svg)](https://codecov.io/gh/engineervix/garmin-activity-share)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Garmin Activity Share](#garmin-activity-share)
  - [Description](#description)
  - [Running the program](#running-the-program)
    - [Pre-requisites](#pre-requisites)
    - [Procedure](#procedure)
  - [Deployment](#deployment)
    - [Dokku](#dokku)
  - [TODO](#todo)
  - [Assets](#assets)
    - [Icons](#icons)
    - [Fonts](#fonts)
    - [Image backgrounds](#image-backgrounds)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

## Description

I was looking for a way to automatically share (primarily tweet, actually) my runs upon completion of a running activity. I could do it from the [Garmin Connect](https://www.garmin.com/en-US/p/125677) app on my phone, but I didn't like the process of selecting a nice image, ensuring proper blending of colours, etc. So I thought automating this would be a fun thing to do!

The result is this project – a python tool that

1. **Connects to your Garmin Connect account** and obtains the last activity (via [python-garminconnect](https://github.com/cyberjunky/python-garminconnect))
2. Uses the data from the last activity to **create an image** (via [Pillow](https://pillow.readthedocs.io/en/stable/))
3. **Sends a tweet** with the image above (via [tweepy](https://www.tweepy.org/))

For this to work, it needs to run periodically, based on your foreseen run days, perhaps as a [cron job](https://en.wikipedia.org/wiki/Cron).

## Running the program

### Pre-requisites

- You need to have a [Twitter developer acount](https://developer.twitter.com/), and a [Garmin Connect](https://connect.garmin.com/) account.
- You need to have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) on your machine:

  ```sh
  # check that you have docker on your machine
  docker -v
  # check that you have docker-compose on your machine
  docker-compose -v
  ```

  If you don't have Docker and Docker Compose, then click the respective links above for installation instructions for your platform.

### Procedure

1. Install dev dependencies in your vitual environment

   ```bash
   # development
   pip install -r requirements-dev.txt
   ```

2. build and spin up docker containers (there are only 2 containers, the `bot` container and the `redis` container. Redis is used to store the retrieved data so that we can make comparisons whenever we fetch data from Garmin Connect. This ensures that we do not share the same result multiple times)

   ```bash
   docker-compose up -d --build
   ```

3. Setup environment variables. See [`env.sample`](.env.sample) for details. Copy `env.sample` to `.env` and update the new file.
4. access the `bot` container: `inv exec bot "bash"`. This is a shortcut for `docker-compose exec bot bash`
5. Inside the container, run `inv tweet`.

## Deployment

### Dokku

Assuming you already have a Dokku machine, all you need to do is

1. create an app
2. install redis and link your app
3. set environment variables
4. remove ports (this isn't a web app)
5. set up persistent storage

The BASH commands below illustrate the above steps.

```bash

# create app
sudo dokku apps:create garmin-activity-share

# setup redis | https://github.com/dokku/dokku-redis
sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis
sudo dokku redis:create redis-garmin-activity-share
sudo dokku redis:link redis-garmin-activity-share garmin-activity-share

# set env variables
sudo dokku config:set --no-restart garmin-activity-share API_KEY=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share API_KEY_SECRET=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share BEARER_TOKEN=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share ACCESS_TOKEN=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share ACCESS_TOKEN_SECRET=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share CLIENT_ID=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share CLIENT_SECRET=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share GARMIN_CONNECT_EMAIL=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share GARMIN_CONNECT_AUTH=xxxxx && \
sudo dokku config:set --no-restart garmin-activity-share MODE=production

# customize Docker Build-time configuration variables
# https://dokku.com/docs/deployment/builders/dockerfiles/#build-time-configuration-variables
sudo dokku docker-options:add garmin-activity-share build '--build-arg MODE=production'

# persistent storage
sudo dokku storage:ensure-directory --chown heroku garmin-activity-share
sudo dokku storage:mount garmin-activity-share /var/lib/dokku/data/storage/garmin-activity-share:/home/tweepy/assets/dist

# remove ports
sudo dokku proxy:ports-remove garmin-activity-share http:80:5000
sudo dokku proxy:ports-remove garmin-activity-share https:443:5000
```

You can adjust the cron schedule in [`app.json`](app.json) to suit your preferences. The default setup is as follows

```bash
# At minute 30 past hour 8 and 20 on every day-of-week from Monday through Saturday.
30 8,20 * * 1-6
```

## TODO

- [ ] Save session to REDIS, instead of a JSON file
- [ ] instead of showing the time as UTC on share image, use local time
- [ ] Fix the PYTHONPATH problem
- [ ] Write tests
- [ ] Share to other platforms
- [ ] Use unsplash API for background images
- [ ] use an API for random quotes
- [ ] improve `Dockerfile` configuration. See <https://stackoverflow.com/questions/43654656/dockerfile-if-else-condition-with-external-arguments>
- [ ] incorporate cron monitoring
- [ ] setup sentry

## Assets

### Icons

- Running person icon: <https://www.svgrepo.com/svg/342791/running>
- Garmin logo: <https://creative.garmin.com/styleguide/resources/logos/>

### Fonts

- [Lato](https://fonts.google.com/specimen/Lato/about)

### Image backgrounds

- [`andrew-slifkin-tL50RgKdn3Q-unsplash.jpg`](assets/unsplash_images/andrew-slifkin-tL50RgKdn3Q-unsplash.jpg) by [Andrew Slifkin](https://unsplash.com/@andrewslifkin?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/tL50RgKdn3Q)
- [`john-t-rPKKiHzLFiY-unsplash.jpg`](assets/unsplash_images/john-t-rPKKiHzLFiY-unsplash.jpg) by [John T](https://unsplash.com/@john_thng?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/rPKKiHzLFiY)
- [`joshua-sortino-XMcoTHgNcQA-unsplash.jpg`](assets/unsplash_images/joshua-sortino-XMcoTHgNcQA-unsplash.jpg) by [Joshua Sortino](https://unsplash.com/@sortino?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/XMcoTHgNcQA)
- [`lucas-favre-JnoNcfFwrNA-unsplash.jpg`](assets/unsplash_images/lucas-favre-JnoNcfFwrNA-unsplash.jpg) by [lucas Favre](https://unsplash.com/@we_are_rising?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/JnoNcfFwrNA)
- [`tara-glaser-WodC5zEcSLQ-unsplash.jpg`](assets/unsplash_images/tara-glaser-WodC5zEcSLQ-unsplash.jpg) by [Tara Glaser](https://unsplash.com/it/@jump2dream?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/WodC5zEcSLQ)
- [`will-suddreth-NRA25SWe71o-unsplash.jpg`](assets/unsplash_images/will-suddreth-NRA25SWe71o-unsplash.jpg) by [Will Suddreth](https://unsplash.com/@willsudds?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/NRA25SWe71o)
- [`andrea-leopardi-QVD3Xht9txA-unsplash.jpg`](assets/unsplash_images/andrea-leopardi-QVD3Xht9txA-unsplash.jpg) by [Andrea Leopardi](https://unsplash.com/@whatyouhide?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/QVD3Xht9txA?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`gary-butterfield-XGKSeGYGP0A-unsplash.jpg`](assets/unsplash_images/gary-butterfield-XGKSeGYGP0A-unsplash.jpg) by [Gary Butterfield](https://unsplash.com/@garybpt?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`zac-ong-RYvOI54rmPw-unsplash.jpg`](assets/unsplash_images/zac-ong-RYvOI54rmPw-unsplash.jpg) by [Zac Ong](https://unsplash.com/@zacong?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`malik-skydsgaard-zZoE-CCid3g-unsplash.jpg`](assets/unsplash_images/malik-skydsgaard-zZoE-CCid3g-unsplash.jpg) by [Malik Skydsgaard](https://unsplash.com/@malikskyds?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`kevin-andre-M2k-Kd4n-S0-unsplash.jpg`](assets/unsplash_images/kevin-andre-M2k-Kd4n-S0-unsplash.jpg) by [Kevin Andre](https://unsplash.com/de/@kevinandrephotography?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`arek-adeoye-gGZ8ZynljWk-unsplash.jpg`](assets/unsplash_images/arek-adeoye-gGZ8ZynljWk-unsplash.jpg) by [Arek Adeoye](https://unsplash.com/@areksan?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`jim-makos-bYy09RkQW8w-unsplash.jpg`](assets/unsplash_images/jim-makos-bYy09RkQW8w-unsplash.jpg) by [Jim Makos](https://unsplash.com/@jimmakos?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`mike-cox-NrhgewTdfF8-unsplash.jpg`](assets/unsplash_images/mike-cox-NrhgewTdfF8-unsplash.jpg) by [Mike Cox](https://unsplash.com/@iprefermike?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/running?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`maxwell-nelson-UvN7K8MM-8k-unsplash.jpg`](assets/unsplash_images/maxwell-nelson-UvN7K8MM-8k-unsplash.jpg) by [Maxwell Nelson](https://unsplash.com/@maxcodes?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/UvN7K8MM-8k?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
- [`will-suddreth-1pjRN2kphIs-unsplash.jpg`](assets/unsplash_images/will-suddreth-1pjRN2kphIs-unsplash.jpg) by [Will Suddreth](https://unsplash.com/@willsudds?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/1pjRN2kphIs?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
