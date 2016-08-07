# Cloud Server Setup

For the final part of the series the cloud server should be a real machine/instance
running in a cloud like Amazon AWS (i.e. no more vagrant virtual server).  You
will need to provision an Ubuntu cloud server somewhere, and be aware that you
might incur costs from running the server, bandwidth it consumes, etc!

Ensure the server has the following ports open to it from the public internet:

-   TCP port 80: This is used for normal web traffic.

-   TCP port 8080: This is used for the MJPEG camera stream.

-   TCP port 22: This is used for SSH connections to manage the server.

Note that you do NOT need to open port 1883 for MQTT communication.  Although
the project uses MQTT and the cloud server hosts the broker, a SSH tunnel is
created on the Raspberry Pi to securely connect to the broker.

Once the server is running you will want to follow the steps below in order to
configure and run the cloud server components:

## MQTT Broker Setup

You will want to setup a MQTT broker on the cloud server that will be used to
send laser control messages to the Pi.  The mosquitto MQTT broker will be used
for this as it is easy to setup and configure.  For now a basic configuration with
no authentication will be used, however it is advised that you explore how to secure
the server when using in a 'production' setting (later videos will cover this topic).

To install mosquitto run the following commands inside the cloud server VM:

    sudo apt-get update
    sudo apt-get install -y mosquitto mosquitto-clients

At this point mosquitto MQTT server will be setup and running with its default
configuration of port 1883 public access.  Be sure your cloud server does NOT
allow this port to be open to the public internet or else anyone could take
control of your cat laser!

## mjpeg-proxy Setup

Follow the README.md in the mjpeg-proxy folder to setup an mjpeg-proxy server
for the Pi camera stream.

## Cloud Laser Server Setup

Follow the README.md in the CloudLaserServer folder to setup the cloud laser
server code.
