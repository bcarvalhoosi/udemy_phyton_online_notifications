import time
import datetime as dt
import smtplib
import random
import requests
import json

POSITION_RANGE = 5  # +5 or -5 degrees for ISS position
KEEP_ALIVE_FILENAME = "keep_alive.txt"
QUOTE_FILENAME = "quotes.txt"
CONFIG_FILENAME = "config.json"

config={}
can_continue = False

try:
    config_file = open(CONFIG_FILENAME, "r")
except FileNotFoundError:
    print("Config file not found. Creating one...")
else:
    config = json.load(config_file)
    config_file.close()
    if config["keep_alive"] == 1:
        try:
            file = open(KEEP_ALIVE_FILENAME,"r")
        except FileNotFoundError:
            can_continue = True
        else:
            last_dt = file.read()
            file.close()
            last_dt = dt.datetime.strptime(last_dt,"%Y-%m-%d %H:%M:%S.%f")
            if last_dt > dt.datetime.now() + dt.timedelta(minutes=-5):
                print("Another process running. Exiting...")
            else:
                can_continue = True
    else:
        can_continue = True

print(f"Program started at {dt.datetime.now()}")

def send_mail(subject, message):
    global config
    with smtplib.SMTP(config["my_smtp_address"], ) as connection:
        connection.starttls()
        connection.login(user=config["my_email"], password=config["my_password"])
        connection.sendmail(
            from_addr=config["my_email"],
            to_addrs=config["mail_to"].split(';'),
            msg=f"Subject:{subject}{message}{config["my_email_signature"]}"
        )
    print(f"Email sent to {config["mail_to"]} at {dt.datetime.now()} with subject {subject} and message {message}")

def send_day_quote():
    global last_day_quote
    if last_day_quote != dt.datetime.now().day and dt.datetime.now().hour == 7:
        last_day_quote = dt.datetime.now().day
        with open(QUOTE_FILENAME,"r") as file:
            quotes=file.readlines()
        quote = random.choice(quotes)
        send_mail("Motivation frase of the day... Enjoy it",f"\n\n{quote.replace(" - ", "\n\n")}")

def is_iss_overhead():
    global config
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
    except (requests.RequestException, ValueError) as error:
        print(f"Error connectiong to the API ISS. {error}")
        return False
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    #Your position is within +5 or -5 degrees of the ISS position.
    if ( float(config["my_lat"])-POSITION_RANGE <= iss_latitude <= float(config["my_lat"])+POSITION_RANGE and
         float(config["my_long"])-POSITION_RANGE <= iss_longitude <= float(config["my_long"])+POSITION_RANGE):
        print("ISS is overhead")
        return True
    else:
        print("ISS is not overhead")
        return False

def is_night():
    global config
    parameters = {
        "lat": config["my_lat"],
        "lng": config["my_long"],
        "formatted": 0,
    }
    try:
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
    except (requests.RequestException, ValueError) as error:
        print(f"Error connectiong to the API Sunrise-Sunset. {error}")
        return False
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now()
    if time_now.hour <= sunrise or time_now.hour >= sunset:
        print("Is night")
        return True
    else:
        print("Is day")
        return False

def is_sky_clear_enough():
    global config
    parameters = {
        "lat": config["my_lat"],
        "lng": config["my_long"],
        "current": "cloud_cover",
        "time_zone": "auto"
    }
    try:
        response = requests.get(url="https://api.open-meteo.com/v1/forecast", params=parameters)
        response.raise_for_status()
    except (requests.RequestException, ValueError) as error:
        print(f"Error connectiong to the API Open-Meteo. {error}")
        return False
    cloud_cover = response.json()["current"]["cloud_cover"]
    if cloud_cover < 30:
        print("Sky clear enough")
        return True
    else:
        print("Sky not clear enough")
        return False
if can_continue:
    last_day_quote = 0
    last_day_iss = 0
    while True:
        print(f"Lets see if now {dt.datetime.now()} have something to do.")
        send_day_quote()
        if  is_iss_overhead() and is_sky_clear_enough() and is_night() and last_day_iss != dt.datetime.now().day:
            last_day_iss = dt.datetime.now().day
            send_mail(
                "The ISS is overhead!",
                "The International Space Station is overhead, it's nighttime, "
                "and the sky is clear enough. Look up to see it!"
            )

        if config["keep_alive"] == 1:
            with open(KEEP_ALIVE_FILENAME, "w") as file:
                file.write(f"{dt.datetime.now()}")
        time.sleep(60)

