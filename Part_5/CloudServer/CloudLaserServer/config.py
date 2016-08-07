# Raspberry Pi Cat Laser 2.0 - Cloud Laser Server Configuration
# Modify the variables below to adjust the cloud laser server configuration.
# Author: Tony DiCola

# Secret key should be set to a random value (like you're making a new password).
# You don't need to remember this value, instead it's used to secure session state.
SECRET_KEY = 'some random secret value!'

# Set MJPEG_URL to the URL of the mjpeg-proxy stream that displays video:
MJPEG_URL = 'http://<your cloud server domain/DNS name>:8080/index1.jpg'

# Amount of time (in seconds) each active player has to play:
PLAYTIME_SECONDS = 60.0

# Hostname for the MQTT server that the Pi will listen to for commands.
MQTT_HOST = 'localhost'
