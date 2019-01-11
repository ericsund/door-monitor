#!/usr/bin/python

import RPi.GPIO as io
import time, sys, os, tweepy
from twython import Twython
from datetime import datetime

# Hardware settings config
gpio_pin = 12

# Defaults to initial state of closed door
# Handles optional arg for initial state of open door
door_change = True
if len(sys.argv) > 1:
	door_change_arg = sys.argv[1]

	if door_change_arg == "--door-open":
		door_change = False
	elif door_change_arg == "--door-closed":
		door_change = True
	else:
		print error + "Arg must be either --door-closed or --door-open"

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
print debug + "READY!"

def sendTweet():
	current_time = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
	update_string = "[ " + current_time + " ] Door was opened."

	sent = False
	while not sent:
		try:
			t.update_status(status = update_string)
			sent = True
		except ConnectionError:
			time.sleep(5)

# Check for door changes
while True:
	try:
		if io.input(gpio_pin) == door_change:
			print debug + "Door changed"
			print debug + "Sending tweet..."
			sendTweet()
			print debug + "Tweet sent"

			door_change = not door_change
		time.sleep(1)
	except Exception as e:
		logging.error(traceback.format_exc())
