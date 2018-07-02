import RPi.GPIO as io
import time

# Settings config
gpio_pin = 12
door_change = True

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
		door_change = not door_change
		time.sleep(1)
