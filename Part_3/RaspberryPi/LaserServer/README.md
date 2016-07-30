# Raspberry Pi Laser Server

This is the original cat laser toy server code which is meant to control the
cat laser through a web page one person can access.  This code is meant to be
used _internally_ and should not be exposed out to the broader internet!  The
reason for keeping this code is that it is necessary to perform calibration or
manually control the laser toy and this server works great for those purposes.

To use the server you must first install a few dependencies by running on the Pi:

    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-dev python3-numpy build-essential
    sudo pip3 install flask

Then start the cat laser server by running in this directory:

    python3 server.py

Once running access it by going to the following URL in a browser (note you might
need to specify the IP address of your Raspberry Pi instead of the hostname):
http://raspberrypi:5000/

Use the calibration process to generate a new calibration.json file for the laser
driver or other tools.
