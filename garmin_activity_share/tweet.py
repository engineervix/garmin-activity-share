import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import pytz
import redis
import tweepy
from dotenv import load_dotenv

from garmin_activity_share import connect, draw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
CONSUMER_KEY = os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REDIS_URL = os.getenv("REDIS_URL")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

client_v1 = tweepy.API(auth, wait_on_rate_limit=True)

client_v2 = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

# Get the directory containing the script
script_dir = Path(__file__).parent

# Get the project directory
project_dir = script_dir.parent


def verify_credentials():
    try:
        client_v1.verify_credentials()
        logger.info("Authentication OK")
    except Exception:
        logger.error("Error during authentication")


def get_time_of_day(time: datetime, timezone: str = "Africa/Lusaka") -> str:
    """
    Returns a string indicating whether the given time is in the morning, afternoon, or evening.
    The given time is expected to be in UTC timezone, and the time of day is determined based
    on the provided `timezone`, default being `Africa/Lusaka`
    """

    if time.tzinfo != pytz.utc:
        time = time.replace(tzinfo=pytz.utc)

    tz = pytz.timezone(timezone)
    time_in_tz = time.astimezone(tz)

    # Get the hour of the day (0-23)
    hour = time_in_tz.hour

    if hour < 12:
        return "morning"
    elif hour < 17:
        return "afternoon"
    else:
        # The hour is between 5pm and midnight
        return "evening"


def get_day_and_time_of_day():
    """
    For example, 'Wednesday evening', or 'Saturday morning'
    """
    r = redis.from_url(REDIS_URL)
    json_str = r.get("last_activity")

    if json_str is not None:
        data = json.loads(json_str)

        start_time_GMT = data["startTimeGMT"]  # e.g 2022-12-29 03:41:52
        start_time_src_fmt = "%Y-%m-%d %H:%M:%S"
        start_time_dt = datetime.strptime(start_time_GMT, start_time_src_fmt).replace(tzinfo=pytz.utc)
        day_of_week = start_time_dt.strftime("%A")
        time_of_day = get_time_of_day(time=start_time_dt, timezone="Africa/Lusaka")

        return f"{day_of_week} {time_of_day}"
    else:
        logger.error("There's no existing data to work with, cannot proceed")
        sys.exit(1)


def main():
    # ===== Here's an example tweet (no image) ===== #
    # client_v2.create_tweet(text="My first tweet powered by #python 🐍 and #tweepy! 😃 🚀\n https://github.com/tweepy/tweepy")

    # ===== And now, tweet with image  ===== #

    # first, perform a simple check before proceeding
    if connect.need_to_get_last_activity():
        # grab last activity
        connect.get_last_activity()

        # create the image to be shared
        draw.create_garmin_share_image()

        image = f"{project_dir}/assets/dist/share.jpg"
        day_and_time_of_day = get_day_and_time_of_day()

        status_options = [
            f"👟 {day_and_time_of_day} run 🏃‍♂️\nPowered by @GarminFitness #BeatYesterday",
            f"👟 {day_and_time_of_day} run 🏃‍♂️",
            f"👟 {day_and_time_of_day} run 🏃‍♂️\n“There are clubs you can’t belong to, neighbours you can’t live in, schools you can’t get into, but the roads are always open.” – @nike",
            f"👟 {day_and_time_of_day} run 🏃‍♂️\n“A run begins the moment you forget you are running.” – @adidas",
            f"🏃‍♂️ {day_and_time_of_day} run 👟\nPowered by @GarminFitness #BeatYesterday",
            f"🏃‍♂️ {day_and_time_of_day} run 👟",
            f"🏃‍♂️ {day_and_time_of_day} run 👟\n“Success isn’t given. It’s earned on the track, the field, the gym. With blood, sweat, and the occasional tear.” – @nike",
            f"🏃‍♂️ {day_and_time_of_day} run 👟\n“If you can't fly then run, if you can't run then walk, if you can't"
            " walk then crawl, but whatever you do you have to keep moving forward”. – Martin Luther King Jr",
        ]

        status = random.choice(status_options)

        try:
            media = client_v1.media_upload(filename=image)
            client_v2.create_tweet(text=status, media_ids=[media.media_id])
            logger.info("Woohoo! Your twitter status has been updated 🚀")
        except Exception as err:
            logger.error("Error encounterd while attempting to update your twitter status: %s", err)

        # cleanup
        try:
            os.remove(image)
        except OSError as ex:  # if failed, report it back to the user
            print(f"Error: {ex.filename} - {ex.strerror}.")


if __name__ == "__main__":
    main()
