# Raspberry Pi Cat Laser 2.0 Cloud Laser Server

This is the Cat Laser 2.0 cloud laser server code which is meant to run in a
cloud server (like an Amazon AWS instance) and allow multiple users to control
the cat laser.  Only one user can control the laser at a time and other connected
users will wait in line for their turn to play for a limited amount of time.

You will need a cloud server running Ubuntu (this code tested on Ubuntu 16.04 LTS)
and with BOTH port 80 and 8080 open from the public internet.  No other ports (beyond
those necessary to control the cloud server, like SSH) are necessary to be open.

To run this code you'll need to first install a few dependencies by running these
commands on the cloud server:

    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-dev nodejs nodejs-legacy npm
    sudo pip3 install flask flask-socketio eventlet

Next copy this CloudLaserServer folder to the cloud server.  You will then need
to modify the config.py file and adjust a few settings inside it:

-   SECRET_KEY: Set this to a random string, like you're setting a password.  You
    don't need to remember this value instead it's used to secure session state.

-   MJPEG_URL: Set this to the full URL for the MJPEG camera stream that mjpeg-proxy
    on the cloud server generates.  This should be something like http://<your cloud server domain/DNS name>:8080/index1.jpg if you're following the same steps.

To run the server you'll first want to make sure the other components of the project
are running:

-   On the Raspberry Pi:

    -    Ensure mjpeg-streamer is running and exposing an MJPEG video stream of
         the Pi camera.

    -    If your Pi is not directly accessible to the internet (i.e. if you're
         at home and the Pi is connected to a router) forward port 8080 from your
         router to the Raspberry Pi.  This will allow outside users (like the
         cloud server) to access the video stream.

    -    Ensure ssh is running to create a tunnel for port 1883 (MQTT) to this
         cloud server.  On the Pi run the following command (you will need to
         adjust the -i option to point at the private key for connecting to your
         cloud server and specify the right username and address for the cloud
         server):

             ssh -nNT -L 1883:localhost:1883 -i /path/to/cloud/server/key.pem user@cloudserver &

         This will run the SSH tunnel in the background and all the Pi to access
         the cloud server's MQTT server securely without a lot of certificate and
         SSL hassle.

    -    Ensure the LaserDriver script is calibrated (using the LaserServer and
         copying over its calibration.json) and running.

-   On the cloud server:

    -    Configure mjpeg-proxy so that it the videoSource value in mjpeg-proxy.js
         is pointing at the URL to your home IP address (use whatismyip.org) and
         the video stream exposed by the Raspberry Pi.  For example if your home
         IP address is 100.200.0.1 then the videoSource URL should look something
         like:

             http://100.200.0.1:8080/?action=stream

         Once configured start mjpeg-proxy running in the background (make sure
         you've already installed the NodeJS dependencies, see the README.md in the
         mjpeg-proxy folder):

             node mjpeg-proxy.js &

    -    Ensure you've updated the CloudLaserServer config.py and set the
         SECRET_KEY and MJPEG_URL values.

    -    Finally start the cloud laser server code by running inside this
         CloudLaserServer directory:

             sudo FLASK_APP=server.py flask run --host 0.0.0.0 --port 80

Once all the components are running access your cloud server domain/DNS name
in a web browser and start playing!
