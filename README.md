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

- [Description](#description)
- [Running the program](#running-the-program)
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

You need to have a [Twitter developer acount](https://developer.twitter.com/), and a [Garmin Connect](https://connect.garmin.com/) account.

1. Install dependencies

   ```bash
   # production
   pip install -r requirements.txt

   # development
   pip install -r requirements-dev.txt
   ```

2. Setup environment variables. See [`env.sample`](.env.sample) for details.
3. `inv tweet`. This is a shortcut for `PYTHONPATH=. python garmin_activity_share/tweet.py`

## TODO

- [ ] Fix the PYTHONPATH problem
- [ ] Write tests
- [ ] Share to other platforms
- [ ] Use unsplash API for background images
- [ ] use an API for random quotes

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
