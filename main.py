__author__ = 'schaef'

import time
import grovepi
from grove_rgb_lcd import *

# get the widgets
from Widgets._list import ListWidget
from Widgets._percentage import PercentageWidget

# MAIN MENU callbacks
def main_menu_callback(value):
    global wid
    if value == 0:
        wid = create_light_percentage()
    if value == 1:
        #wid = create_light_percentage()
        pass
    if value == 2:
        wid = create_light_switch_menu()

def create_main_menu():
    my_list = ["Change brightness", "Change scene", "Switch light on/off"]
    return ListWidget(my_list, main_menu_callback)

# light switch menu
def light_switch_menu_callback(value):
    global wid
    if value == 0:
        pass # TODO:
    if value == 1:
        pass # TODO:
    wid = create_main_menu()

def light_switch_menu_cancel_callback():
    global wid
    wid = create_main_menu()

def create_light_switch_menu():
    my_list = ["On", "Off"]
    return ListWidget(my_list, light_switch_menu_callback, light_switch_menu_cancel_callback)


# Light percentage callback
def light_percentage_callback(value):
    global wid
    wid = create_main_menu()
    pass

def create_light_percentage():
    return PercentageWidget(light_percentage_callback, "Change brightness")

# This is the main variable holding the current widget.
wid = create_main_menu()


# now grove related LED stuff
MY_DISPLAY_OFF = 0
MY_DISPLAY_ON = 1
MY_DISPLAY_WAIT = 2


color_red = 0
color_green = 120
color_blue = 120
fade = 1.0

# Connect the Grove Ultrasonic Ranger to digital port D7
# SIG,NC,VCC,GND
ultrasonic_ranger = 7


# initialize the blank display
is_on = MY_DISPLAY_OFF
setText("nothing")
setRGB(0,0,0)

# set up the rotary sensor =======================
# Connect the Grove Rotary Angle Sensor to analog port A1
# SIG,NC,VCC,GND
potentiometer = 1


grovepi.analogWrite(4,0)
#grovepi.analogWrite(2,0)

grovepi.pinMode(potentiometer,"INPUT")

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300

# button =================================
# Connect the Grove Button to digital port D2
# SIG,NC,VCC,GND
button = 2
grovepi.pinMode(button, "INPUT")


# Helper stuff =====================

delta_time = time.time()
degrees = 0
old_degrees = degrees
button_down = False

try:
    while True:
        try:

            if grovepi.ultrasonicRead(ultrasonic_ranger) < 80:

                # click
                if grovepi.digitalRead(button):
                    if not button_down:
                        wid.click()
                    button_down = True
                else:
                    button_down = False

                #read the rotary sensor
                # Read sensor value from potentiometer
                sensor_value = grovepi.analogRead(potentiometer)
                # Calculate voltage
                voltage = round((float)(sensor_value) * adc_ref / 1023, 2)
                # Calculate rotation in degrees (0 to 300)
                degrees = round((voltage * full_angle) / grove_vcc, 2)
                wid.dial(degrees)


                if is_on is MY_DISPLAY_OFF or wid.is_dirty():
                    #refresh the display
                    wid.refresh()
                    dirty = False
                # restore brightness and set all falgs to on.e
                setRGB(color_red,color_green,color_blue)
                is_on = MY_DISPLAY_ON
                fade = 1.0
            else:
                if is_on == MY_DISPLAY_ON:
                    delta_time = time.time()
                    is_on = MY_DISPLAY_WAIT
                if is_on == MY_DISPLAY_WAIT and (time.time()-delta_time)>3:
                    setText("nothing")
                    setRGB(0,0,0)
                    is_on = MY_DISPLAY_OFF
                    print "off"
                elif is_on == MY_DISPLAY_WAIT and (time.time()-delta_time)>0.5:
                    fade *= 0.5
                    new_red = int(float(color_red)*fade)
                    new_green = int(float(color_green)*fade)
                    new_blue = int(float(color_blue)*fade)
                    setRGB(new_red,new_green,new_blue)

        except TypeError:
            pass
        except IOError:
            pass

except KeyboardInterrupt:
    setText("nothing")
    setRGB(0,0,0)
