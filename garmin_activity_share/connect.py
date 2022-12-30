import io
import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
GARMIN_CONNECT_EMAIL = os.getenv("GARMIN_CONNECT_EMAIL")
GARMIN_CONNECT_AUTH = os.getenv("GARMIN_CONNECT_AUTH")


def display_json(api_call, output):
    """Format API output for better readability."""

    dashed = "-" * 20
    header = f"{dashed} {api_call} {dashed}"
    footer = "-" * len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        # Try to load the previous session
        with open("session.json") as f:
            saved_session = json.load(f)

            print("Login to Garmin Connect using session loaded from 'session.json'...\n")

            # Use the loaded session for initializing the API (without need for credentials)
            api = Garmin(session_data=saved_session)

            # Login using the
            api.login()

    except (FileNotFoundError, GarminConnectAuthenticationError):
        # Login to Garmin Connect portal with credentials since session is invalid or not present.
        print(
            "Session file not present or turned invalid, login with your Garmin Connect credentials.\n"
            "NOTE: Credentials will not be stored, the session cookies will be stored "
            "in 'session.json' for future use.\n"
        )
        try:
            api = Garmin(GARMIN_CONNECT_EMAIL, GARMIN_CONNECT_AUTH)
            api.login()

            # Save session dictionary to json file for future use
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(api.session_data, f, ensure_ascii=False, indent=4)
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error("Error occurred during Garmin Connect communication: %s", err)
            return None

    return api


def need_to_get_last_activity() -> bool:
    """
    Check if it's necessary to get last activity
    """
    # Get the directory containing the script
    script_dir = Path(__file__).parent
    # Get the project directory
    project_dir = script_dir.parent

    data = project_dir / "data.json"
    if data.exists():
        with open(data) as f:
            existing_data = json.load(f)
        api = init_api(GARMIN_CONNECT_EMAIL, GARMIN_CONNECT_AUTH)
        activity = api.get_last_activity()
        new_data = json.dumps(activity)
        return existing_data != json.loads(new_data)
    else:
        return True


def get_last_activity():
    """
    connect to Garmin Connect, fetch latest activity and save
    it as a timestamped JSON file in project directory
    """
    # Init API
    api = init_api(GARMIN_CONNECT_EMAIL, GARMIN_CONNECT_AUTH)

    # Get last activity
    activity = api.get_last_activity()
    display_json("api.get_last_activity()", activity)

    # save it as a JSON file
    with io.open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(activity, indent=4))
