import time
import datetime as dt
import smtplib
import random
import requests

MY_LAT = 0 # Your latitude
MY_LONG = 0 # Your longitude
MAIL_TO = "" # the emails you want, ; separated
last_day_quote = 0
last_day_iss = 0

print(f"Program started at {dt.datetime.now()}")

def send_mail(subject, message):
    my_email="" # your email used to send messages
    my_password="" # aplication password. google it to find how you get and app password to put here
    with smtplib.SMTP('smtp.gmail.com', ) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=MAIL_TO.split(';'),
            msg=f"Subject:{subject}{message}\n\nBest regards,\nfrom your beloved\nBernardino Carvalho"
        )
    print(f"Email sent to {MAIL_TO} at {dt.datetime.now()} with subject {subject} and message {message}")

def send_day_quote():
    global last_day_quote
    if last_day_quote != dt.datetime.now().day and dt.datetime.now().hour == 7:
        last_day_quote = dt.datetime.now().day
        with open("quotes.txt","r") as file:
            quotes=file.readlines()
        quote = random.choice(quotes)
        send_mail("Motivation frase of the day... Enjoy it",f"\n\n{quote.replace(" - ", "\n\n")}")

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    #Your position is within +5 or -5 degrees of the ISS position.
    if ( MY_LAT-5 <= iss_latitude <= MY_LAT+5 and
         MY_LONG-5 <= iss_longitude <= MY_LONG+5):
        print("ISS is overhead")
        return True
    else:
        print("ISS is not overhead")
        return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
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
    parameters = {
        "latitude": MY_LAT,
        "longitude": MY_LONG,
        "current": "cloud_cover",
        "time_zone": "auto"
    }
    response = requests.get(url="https://api.open-meteo.com/v1/forecast", params=parameters)
    response.raise_for_status()
    cloud_cover = response.json()["current"]["cloud_cover"]
    if cloud_cover < 30:
        print("Sky clear enough")
        return True
    else:
        print("Sky not clear enough")
        return False

while True:
    print(f"Lets see if now {dt.datetime.now()} have something to do.")
    send_day_quote()
    if  is_iss_overhead() and is_sky_clear_enough() and is_night() and last_day_iss != dt.datetime.now().day:
        last_day_iss = dt.datetime.now().day
        send_mail("A Estação Espacial Internacional está mesmo por cima de nós...","A Estação Espacial Internacional está mesmo por cima de nós, já é de noite e há poucas ou nenhumas nuvens, por isso é uma boa oportunidade para a ver. Basta olhar para cima.")
    time.sleep(60)

