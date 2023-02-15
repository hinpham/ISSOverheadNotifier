import requests
from datetime import datetime
import smtplib
import time
email = "EMAIL_HERE"
password = "PASSWORD_HERE"
MY_LAT = 29.956060
MY_LONG = -95.511000

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
def within_margin():
    return abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LONG - iss_longitude) <= 5

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}



#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
def is_dark():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    
    return time_now.hour >= sunset or time_now.hour <= sunrise


while True:
    time.sleep(60) #Run the code every 60s
    if within_margin() and is_dark():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg="Subject:Look Up\n\nThe ISS is above you."
        )
