# Raspberry Pi Cat Laser 2.0 - Cloud Laser Server
# Flask & Flask-SocketIO application that allows multiple users to spectate and
# play with the cat laser.  Only one player can be active at a time (identified
# by IP address) and other players will wait in line for their turn to play.
# Author: Tony DiCola
import collections
import json
import sys
import threading
import time

from flask import *
from flask_socketio import *
import paho.mqtt.publish as publish

import config
import players


# Initialize flask app
app = Flask(__name__)
app.config.from_object(config)
socketio = SocketIO(app)

# Global state, keep an ordered dict of all the active players (i.e. people waiting to
# play with the cat laser).  The key for each user is their IP address so multiple
# tabs open will still only give them one spot in line.
laser_players = players.Players(app.config['PLAYTIME_SECONDS'])
players_thread = None


# Helper functions:
def notify_wait_position():
    """Broadcast to each waiting player their current position in line."""
    for i, ip in enumerate(laser_players.enumerate_players()):
        # Make i 1-based instead of 0-based since the first person is actually
        # at position 1 instead of 0 in line.
        socketio.emit('wait_position', i+1, room=ip)

def start_active(ip):
    """Callback that's invoked when a player becomes the active player.  Will
    send a socketio message to notify them of being active.
    """
    socketio.send('start_active', room=ip)

def end_active(ip):
    """Callback that's invoked when a player stops being active (i.e. their
    playtime ends).  Will send a socketio message to notify the active player,
    and will send a message to all waiting players with their new position in
    line.
    """
    socketio.send('end_active', room=ip)
    notify_wait_position()

def process_players():
    """Function to update the play state for the active and waiting players.
    Should be called as a background thread to run forever and update the game
    state for active and waiting players.
    """
    last = time.time()
    while True:
        # Find out the elapsed time since the last loop iteration.
        current = time.time()
        elapsed = current - last
        last = current
        # First push out a message to the active player with their remaining
        # playtime.
        active = laser_players.active_player()
        if active is not None:
            ip, remaining = active
            socketio.emit('playtime', remaining, room=ip)
        # Next update the game state, firing any start or end active player
        # callback when appropriate.
        laser_players.update(elapsed, start_active, end_active)
        # Wait a bit and repeat!
        socketio.sleep(0.25)


# Flask routes & socket IO events:
@app.route('/')
@app.route('/spectate')
def spectate():
    """Spectator mode displays video and a link to play."""
    return render_template('spectate.html')

@app.route('/play')
def play():
    """Play mode allows a user to wait in line for their turn to play."""
    return render_template('play.html')

@socketio.on('connect')
def connect():
    """Called when a user in play mode connects to socket IO."""
    print('Connect! {0}'.format(request.remote_addr))
    # Check if the background process to manage active players is running, and
    # if not spin it up.
    global players_thread
    if players_thread is None:
        players_thread = socketio.start_background_task(target=process_players)
    # Add each session to a room based on the user's IP address.  This lets
    # the server easily address all of the same user's sessions by sending
    # data to their room.
    ip = request.remote_addr
    join_room(ip)
    # Update the game state for this player.
    laser_players.add_player(ip)
    # Broadcast to the player their current waiting position in line.
    position = laser_players.wait_position(ip)
    if position is not None:
        # Bump wait position by 1 so it's 1-based instead of 0-based index.
        socketio.emit('wait_position', position+1, room=ip)

@socketio.on('disconnect')
def disconnect():
    """Called when a user disconnects the socket IO connection."""
    # Update the game state for this player.
    ip = request.remote_addr
    laser_players.remove_player(ip)
    # Let all the waiting players know their new position in line.
    notify_wait_position()

@socketio.on('target')
def target(message):
    """Socket IO event sent when a user clicks to target the cat laser."""
    # Check if the player who sent this target request is active and still
    # playing (i.e. has remaining playtime).
    ip = request.remote_addr
    active = laser_players.active_player()
    if active is None:
        return  # Player isn't active, stop processing.
    active_ip, remaining = active
    if active_ip == ip and remaining >= 0.0:
        # Grab the target x, y coordinates and send a MQTT target message to
        # the Pi.
        x = message['x']
        y = message['y']
        print('Target: {0}, {1}'.format(x, y))
        publish.single("catlaser/target", "{0},{1}".format(x, y),
                       hostname=app.config['MQTT_HOST'])


if __name__ == '__main__':
    socketio.run(app)
