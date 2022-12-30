import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import pytz
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

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Get the directory containing the script
script_dir = Path(__file__).parent

# Get the project directory
project_dir = script_dir.parent


def verify_credentials():
    try:
        api.verify_credentials()
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
    json_file = project_dir / "data.json"
    if json_file.exists():
        with open(json_file) as f:
            data = json.load(f)

        start_time_GMT = data["startTimeGMT"]  # e.g 2022-12-29 03:41:52
        start_time_src_fmt = "%Y-%m-%d %H:%M:%S"
        start_time_dt = datetime.strptime(start_time_GMT, start_time_src_fmt).replace(tzinfo=pytz.utc)
        day_of_week = start_time_dt.strftime("%A")
        time_of_day = get_time_of_day(time=start_time_dt, timezone="Africa/Lusaka")

        return f"{day_of_week} {time_of_day}"
    else:
        logger.error("The data.json file doesn't exist, cannot proceed")
        sys.exit(1)


def main():
    # ===== Here's an example tweet (no image) ===== #
    # api.update_status("My first tweet powered by #python 🐍 and #tweepy! 😃 🚀\n https://github.com/tweepy/tweepy")

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
            f"👟 {day_and_time_of_day} run 🏃‍♂️\n Powered by @GarminFitness #BeatYesterday",
            f"👟 {day_and_time_of_day} run 🏃‍♂️",
            f"👟 {day_and_time_of_day} run 🏃‍♂️\n “Someone who is busier than you is running right now.” – @nike",
            f"🏃‍♂️ {day_and_time_of_day} run 👟\n Powered by @GarminFitness #BeatYesterday",
            f"🏃‍♂️ {day_and_time_of_day} run 👟",
            f"🏃‍♂️ {day_and_time_of_day} run 👟\n “If you can't fly then run, if you can't run then walk, if you can't"
            " walk then crawl, but whatever you do you have to keep moving forward”. – Martin Luther King Jr",
        ]

        status = random.choice(status_options)

        try:
            media = api.media_upload(filename=image)
            api.update_status(status=status, media_ids=[media.media_id])
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
