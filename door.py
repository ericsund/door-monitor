#!/usr/bin/python

import RPi.GPIO as io
import time, sys, os, tweepy
from twython import Twython
from datetime import datetime

# Hardware settings config
gpio_pin = 12
door_change = True

# Twitter API settings config
keys_file = open("keys", "r")
keys = []
for key in keys_file:
	key = key[:-1]
	keys.append(key)

t = Twython(keys[0], keys[1], keys[2], keys[3])

# Setup message types
error = "[ERROR] "
debug = "[DEBUG] "

print debug + "Initializing hardware"
io.setmode(io.BOARD)
io.setup(gpio_pin, io.IN, pull_up_down=io.PUD_UP)

# Check for door changes
while True:
	if io.input(gpio_pin) == door_change:
		print debug + "Door changed"
		print debug + "Sending tweet..."
				
		current_time = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
		update_string = "[ " + current_time + " ] Door was opened."
		t.update_status(status = update_string)
		print debug + "Tweet sent"

		door_change = not door_change
		time.sleep(1)





