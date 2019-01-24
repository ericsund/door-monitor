#!/usr/bin/python

import RPi.GPIO as io
import time, sys, os, tweepy
from twython import Twython
from datetime import datetime

# Setup initial open door state
magnets_apart = True
door_open = True
initial_state = True
if len(sys.argv) > 1:
	magnets_arg = sys.argv[1]

	if magnets_arg == "--door-open":
		pass # already in initial open door state
	elif magnets_arg == "--door-closed":
		door_open = False
		magnets_apart = False
	else:
		print error + "Arg must be either --door-closed or --door-open"

# Setup Twitter API keys
keys_file = open("keys", "r")
keys = []
for key in keys_file:
	key = key[:-1]
	keys.append(key)

t = Twython(keys[0], keys[1], keys[2], keys[3])

# Setup message types
error = "[ERROR] "
debug = "[DEBUG] "

# Setup hardware
print debug + "Initializing hardware"
gpio_pin = 12
io.setmode(io.BOARD)
io.setup(gpio_pin, io.IN, pull_up_down=io.PUD_UP)
print debug + "READY!"

"""
Sends a tweet when the door state has changed with the date and time
"""
def sendTweet(door_state):
	current_time = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
	
	update_string = ""
	if door_state == True: # door_open = True
		update_string = "[ " + current_time + " ] Door was opened"
	elif not door_state: # door_open = False
		update_string = "[ " + current_time + " ] Door was closed"

	sent = False
	while not sent:
		try:
			t.update_status(status = update_string)
			sent = True
		except ConnectionError:
			time.sleep(5)
"""
Plays a sound when the door state has changed.
"""
def play_doorbell(audio_file_path):
	os.system("omxplayer " + audio_file_path)

# Main
while True:
	try:
		print("pin signal " + str(io.input(gpio_pin)))
		if io.input(gpio_pin) == magnets_apart:
			
			# close a currently open door
			if door_open:
				if not initial_state:
					door_open = False
					print debug + "Sending tweet door closed..."
					play_doorbell("windows_out.mp3")
					sendTweet(door_open)
					print debug + "Tweet sent!"
					magnets_apart = True
				elif initial_state:
					initial_state = False
					magnets_apart = False
			# open a currenly closed door
			elif not door_open:
				if not initial_state:
					door_open = True
					print debug + "Sending tweet door open..."
					play_doorbell("windows_in.mp3")
					sendTweet(door_open)
					print debug + "Tweet sent!"
					magnets_apart = False
				elif initial_state:
					initial_state = False
					magnets_apart = True
					

		time.sleep(1)
	except Exception as e:
		logging.error(traceback.format_exc())
