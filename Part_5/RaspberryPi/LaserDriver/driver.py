# Raspberry Pi Cat Laser Driver
# This code controls the laser pointer servos to target the laser at different
# locations.  Make sure to modify the MQTT_SERVER variable below so that it points
# to the name or IP address of the host computer for the cloud server VM (i.e. the
# machine running the Vagrant virtual machine that has the MQTT broker).
# Author: Tony DiCola
import sys

import model
import servos

import paho.mqtt.client as mqtt
import parse


# Configuration:
SERVO_I2C_ADDRESS     = 0x40   # I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL   = 0      # Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL   = 1      # Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ        = 50     # PWM frequency for the servos in HZ (should be 50)
SERVO_MIN             = 150    # Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX             = 600    # Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER          = 200    # Center value for the servo, should be 0 degrees of rotation.
MQTT_SERVER           = 'tony-imac'  # MQTT server to connect to for receiving commands.
MQTT_PORT             = 1883         # Port for the MQTT server.

# MQTT topics used for controlling the laser.
TOPIC_TARGET          = 'catlaser/target'

# Create servo and laser movement model.
servos = servos.Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)
model = model.LaserModel(servos, SERVO_MIN, SERVO_MAX, SERVO_CENTER)


# MQTT callbacks:
def on_connect(client, userdata, flags, rc):
    # Called when connected to the MQTT server.
    print('Connected to MQTT server!')
    # Subscribe to the laser targeting topic.
    client.subscribe(TOPIC_TARGET)

def on_message(client, userdata, msg):
    # Called when a MQTT message is received.
    print('{0}: {1}'.format(msg.topic, str(msg.payload)))
    # Handle a target request.
    if msg.topic == TOPIC_TARGET:
        # Try to parse out two numbers from the payload.  These are the
        # screen x and screen y coordinates for the target command.
        result = parse.parse('{:d},{:d}', msg.payload.decode('ascii'))
        if result is not None:
            # Got a valid pair of numbers, use the laser model to target that
            # position.
            model.target(result[0], result[1])

def on_disconnect(client, userdata, rc):
    # Called when disconnected by the MQTT server.  For now just prints out the
    # result code/reason for disconnecting and quits.
    print('Disconnected with rc: {0}'.format(rc))
    sys.exit(1)


# Setup MQTT client and connect to server.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Run a loop in the foreground that waits for MQTT events/messages and processes
# them appropriately with the callbacks above.  The loop_forever call will never
# return!
print('Press Ctrl-C to quit...')
client.loop_forever()
