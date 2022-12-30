import glob
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def create_garmin_share_image():
    """
    create an image with stats from your activity

    Core stats needed (with example data):
        -   "activityName": "Lusaka Running"
        -   "distance": 15519.23046875,
        -   "duration": 6301.21484375,
        -   "averageSpeed": 2.4630000591278076,
        -   "startTimeGMT": "2022-12-29 03:41:52",
        -   "locationName": "Lusaka",

    Additional data that may be of interest
        -   "elapsedDuration": 6301.21484375,
        -   "movingDuration": 6298.014007568359,
        -   "elevationGain": 21.0955810546875,
        -   "elevationLoss": 28.8348388671875,
        -   "activityType": {
                "typeKey": "running",
            }
        -   "eventType": {
                "typeKey": "uncategorized",
            },
    """

    # Get the directory containing the script
    script_dir = Path(__file__).parent

    # Get the project directory
    project_dir = script_dir.parent

    json_file = project_dir / "data.json"

    with open(json_file) as f:
        data = json.load(f)

    # here's the raw data
    activity_name = data["activityName"]
    distance = data["distance"]  # in metres
    duration = data["duration"]  # in seconds
    average_speed = data["averageSpeed"]  # in m/s
    start_time_GMT = data["startTimeGMT"]  # e.g 2022-12-29 03:41:52
    location_name = data["locationName"]  # e.g. Lusaka

    # first, we format the data before drawing it on an image

    # 1. distance
    formatted_distance = f"{(distance / 1000):.2f} km"

    # 2. average speed
    minutes_per_km = (1000 / average_speed) / 60
    minutes = minutes_per_km % 60
    seconds = (minutes * 60) % 60
    formatted_average_speed = f'{"%d:%02d" % (minutes, seconds)}/km'

    # 3. duration
    formatted_duration = str(timedelta(seconds=int(duration)))
    if formatted_duration.startswith("0"):
        formatted_duration = formatted_duration[2:]  # remove '0:'

    # 4. start time (well, datetime, actually!)
    start_time_src_fmt = "%Y-%m-%d %H:%M:%S"
    start_time_dest_fmt = "%b %d, %Y, %H:%M UTC"
    start_time_dt = datetime.strptime(start_time_GMT, start_time_src_fmt)
    formatted_start_time = start_time_dt.strftime(start_time_dest_fmt)

    # 5. datetime @ location
    date_time_place = f"{formatted_start_time} @ {location_name}"

    # now, we pick a random background image
    # these images have dimensions 1024 x 1024

    background_image_list = glob.glob(f"{project_dir}/assets/unsplash_images/*.jpg")
    random_image = random.choice(background_image_list)

    # use Pillow to add text to our random image

    # -- 1. First, we "stamp" the image
    # the stamp is a transparent image with a garmin logo on RHS and an activity
    # icon (for now, it's just a running icon) somewhere near the bottom
    # it has the  same dimensions as the selected random image.

    base_image = Image.open(random_image)
    stamp = Image.open(f"{project_dir}/assets/stamp.png")
    width, height = base_image.size  # get size of image
    transparent = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    transparent.paste(base_image, (0, 0))
    transparent.paste(stamp, (0, 0), mask=stamp)
    transparent.convert("RGB").save(f"{project_dir}/assets/dist/canvas.jpg")

    # -- 2. Then, we add text

    canvas = Image.open(f"{project_dir}/assets/dist/canvas.jpg")

    # Create an ImageDraw object
    draw = ImageDraw.Draw(canvas)

    # Choose fonts
    static_content_font = ImageFont.truetype(f"{project_dir}/assets/fonts/Lato/Lato-Black.ttf", 36)
    main_content_font = ImageFont.truetype(f"{project_dir}/assets/fonts/Lato/Lato-Bold.ttf", 57)
    italic_content_font = ImageFont.truetype(f"{project_dir}/assets/fonts/Lato/Lato-BoldItalic.ttf", 51)
    smaller_content_font = ImageFont.truetype(f"{project_dir}/assets/fonts/Lato/Lato-Bold.ttf", 36)

    # define coordinates
    start_x = 27.500
    start_x_offset = start_x + 55.000
    start_y = 57.000
    y_gap = 39.000  # gap between static_content and main_content [this combination is a segment]
    y_segment_offset = 85.000  # gap between segments

    # font colour (RGB)
    fill = (255, 255, 255)

    # Write text on the image
    draw.text((start_x, start_y), "DISTANCE", font=static_content_font, fill=fill)
    draw.text((start_x, start_y + y_gap), formatted_distance, font=main_content_font, fill=fill)

    draw.text((start_x, start_y + y_gap + y_segment_offset), "TIME", font=static_content_font, fill=fill)
    draw.text(
        (start_x, start_y + y_segment_offset + (2 * y_gap)), formatted_duration, font=main_content_font, fill=fill
    )

    draw.text((start_x, start_y + (2 * y_segment_offset) + (2 * y_gap)), "PACE", font=static_content_font, fill=fill)
    draw.text(
        (start_x, start_y + (2 * y_segment_offset) + (3 * y_gap)),
        formatted_average_speed,
        font=main_content_font,
        fill=fill,
    )

    draw.text((start_x_offset, 897.000), activity_name, font=italic_content_font, fill=fill)
    draw.text((start_x, 967.000), date_time_place, font=smaller_content_font, fill=fill)

    # Save the image
    canvas.save(f"{project_dir}/assets/dist/share.jpg")

    # cleanup
    try:
        os.remove(f"{project_dir}/assets/dist/canvas.jpg")
    except OSError as ex:  # if failed, report it back to the user
        print(f"Error: {ex.filename} - {ex.strerror}.")
