# Raspberry Pi Cat Laser Cloud Server
# Flask and Flask-socketio web appplication that allows control of the cat laser
# from the cloud server.  Allows multiple users to connect and start contolling
# the cat laser.
#
# Note you'll want to run this with flask using a command like:
#   FLASK_APP=server.py FLASK_DEBUG=1 flask run --host "0.0.0.0"
#
# Author: Tony DiCola
import json
import sys

from flask import *
from flask_socketio import SocketIO
import paho.mqtt.publish as publish


# Initialize flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# Spectate mode is the default view.
@app.route('/')
@app.route('/spectate')
def spectate():
    return render_template('spectate.html')

# Play mode for people playing with the laser.
@app.route('/play')
def play():
    return render_template('play.html')

@socketio.on('target')
def target(message):
    # Target function is called when the 'target' socketio event is received.
    # This event includes a dictionary with the x, y coordinates of the target
    # (i.e. where the user clicked on the screen).
    # Grab the x, y coordinates and print them out.
    x = message['x']
    y = message['y']
    print('Target: {0}, {1}'.format(x, y))
    # Now publish a catlaser target message with the x, y coordinates to the
    # MQTT broker running on the server.  This message will be routed to the
    # laser driver script running on the Pi and the laser servos will move!
    publish.single("catlaser/target", "{0},{1}".format(x, y), hostname="localhost")

# Start running the flask app
if __name__ == '__main__':
    socketio.run(app)
