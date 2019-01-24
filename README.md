# Door Monitor

This is a Python + Raspberry Pi project which checks if your door is open or closed.  Magnetic switches will come in contact to trigger actions.

### Requirements
* Raspberry Pi
* Breadboard
* 2 jumper wires
* 1 resistor
* 1 magnetic switch
* 1 WiFi dongle (for older Pis)

### Setup
* Go to apps.twitter.com and create an application.
* Copy your consumer keys and access keys into a file called keys, in the repo root dir.
* Connect and wire your Raspberry Pi, see http://pinout.xyz/.  This project uses GPIO pin 12.
* Run the Python script: `sudo python main.py`

### Features
* Send a tweet with the date and time when door is opened and closed
* Play a door open and close sound

### Todo
* Include wiring instructions
