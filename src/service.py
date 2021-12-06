from time import sleep
from sense_hat import SenseHat

sense = SenseHat()

sleep_time = 1

def show_message(text_string, scroll_speed=.1, text_colour=[255, 255, 255], back_colour=[0, 0, 0]):
    sense.set_rotation(180)
    sense.show_message(text_string, scroll_speed, text_colour, back_colour)

def up_pressed(InputEvent):
    if InputEvent.action == 'released':
        global sleep_time
        sleep_time = sleep_time + 1
        show_message(str(sleep_time))

def down_pressed(InputEvent):
    if InputEvent.action == 'released':
        global sleep_time
        if sleep_time > 1:
            sleep_time = sleep_time - 1
        show_message(str(sleep_time))

try:

    # Inverting up and down because of the PI board location at my desk
    sense.stick.direction_up = down_pressed
    sense.stick.direction_down = up_pressed
    sense.stick.direction_middle = sense.clear

    while True:
        # Take readings from all three sensors
        t = sense.get_temperature()
        p = sense.get_pressure()
        h = sense.get_humidity()

        # Round the values to one decimal place
        t = round(t, 2)
        p = round(p, 2)
        h = round(h, 2)

        # Create the message
        # str() converts the value to a string so it can be concatenated
        message = "T: " + str(t) + " P: " + str(p) + " H: " + str(h)

        # Display the scrolling message
        show_message(message, scroll_speed=0.05)

        sleep(sleep_time)

finally:
    sense.clear()
