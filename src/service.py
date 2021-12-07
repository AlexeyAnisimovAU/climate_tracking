from datetime import datetime
from datetime import timedelta
from time import sleep
from sense_hat import SenseHat
from pymongo import MongoClient
from pyowm import OWM

# Constants
connection_string = 'Your connection string'
owm_api_key = 'Your openweathermap.org API key'

# Sydney: 2147714
# New York: 5128581
# Sutherland: 2147804
# Engadine: 2167312
# ID from http://bulk.openweathermap.org/sample/city.list.json.gz;
# unzip the gz file and find your city
location_id = 2167312

# Global variables
sleep_time = 1
fetch_timedelata = timedelta(minutes = 5)
sense = SenseHat()
owm = OWM(owm_api_key)
mgr = owm.weather_manager()

# Methods
def show_message(text_string, scroll_speed=.1, text_colour=[255, 255, 255], back_colour=[0, 0, 0]):
    # Scroll message on the SenseHat screen
    sense.set_rotation(180)
    sense.show_message(text_string, scroll_speed, text_colour, back_colour)

def up_pressed(InputEvent):
    # Handle SenseHat joystic up press
    if InputEvent.action == 'released':
        global sleep_time
        sleep_time = sleep_time + 1
        show_message(str(sleep_time))

def down_pressed(InputEvent):
    # Handle SenseHat joystic down press
    if InputEvent.action == 'released':
        global sleep_time
        if sleep_time > 1:
            sleep_time = sleep_time - 1
        show_message(str(sleep_time))

def fetch_weather():
    # Fetch weather from open weather map
    observation = mgr.weather_at_id(location_id)
    weather_at_location = observation.weather
    weather_at_location_time = datetime.now()

    return weather_at_location, weather_at_location_time

def take_readings():
    # Take readings from the Sense hat sensors
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    # Round the values
    t = round(t, 2)
    p = int(round(p))
    h = int(round(h))
    return t,p,h

def insert_entry(t, p, h, weather_at_location, col):
    # Insert a new entry into the cluster
    indoor = {}
    indoor['t'] = t
    indoor['p'] = p
    indoor['h'] = h

    outdoor = {}
    # {'temp': 26.19, 'temp_max': 28.31, 'temp_min': 23.3, 'feels_like': 26.19, 'temp_kf': None}
    outdoor['t'] = weather_at_location.temperature('celsius')['temp']
    # {'press': 1009, 'sea_level': None}
    outdoor['p'] = weather_at_location.barometric_pressure()['press']
    outdoor['h'] = weather_at_location.humidity

    entry = {}
    entry['time'] = datetime.now()
    entry['indoor'] = indoor
    entry['outdoor'] = outdoor

    col.insert_one(entry)

# Main implementation
try:

    # Get climate_tracking collection
    client = MongoClient(connection_string)
    db = client.climate_db
    col = db.climate_tracking

    # Init SenseHat joystic handlers
    # Inverting up and down because of the PI board location at my desk
    sense.stick.direction_up = down_pressed
    sense.stick.direction_down = up_pressed
    sense.stick.direction_middle = sense.clear

    # Get initial weather information for the location
    weather_at_location, weather_at_location_time = fetch_weather()

    show_message('Starting...')
    
    while True:
        # Take readings from SenseHat
        t, p, h = take_readings()

        # Fetch outdoor readings
        if datetime.now() > weather_at_location_time + fetch_timedelata:
            weather_at_location, weather_at_location_time = fetch_weather()

        # Insert entry into the cluster
        insert_entry(t, p, h, weather_at_location, col)

        # Wait for the next beat
        sleep(sleep_time)

finally:
    sense.clear()
