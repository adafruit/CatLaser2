# mjpeg-streamer Setup

These instructions describe how to setup the mjpeg-streamer tool to stream the
Raspberry Pi camera as a MJPEG (motion-JPEG) video stream.  This type of video
stream is perfect for the project because it is very low latency and can be
used in a webpage without any plugins or web security model issues.

The version of mjpeg-streamer used here is a special fork with Raspberry Pi
camera support added to it and is available on GitHub at: https://github.com/jacksonliam/mjpg-streamer

To install run the following commands on the Pi:

    sudo apt-get update
    sudo apt-get install -y build-essential git libjpeg62-turbo-dev
    cd ~
    git clone https://github.com/jacksonliam/mjpg-streamer.git
    cd mjpeg-streamer
    cd mjpeg-streamer-experimental
    make
    sudo make install

You can then run the tool manually with the following command in the same
mjpeg-streamer-experimental directory:

    LD_LIBRARY_PATH=. ./mjpg_streamer -i "./input_raspicam.so -vf -fps 30" -o "./output_http.so -w ./www"

Notice the -vf and -fps 30 options for the input_raspicam.so plugin.  The -vf
option performs a vertical flip of the camera output which may or may not be required
for your setup.  The -fps 30 option runs the camera video at 30 frames per second
for a faster update rate.  You can explore other options to the camera plugin
here: https://github.com/jacksonliam/mjpg-streamer/blob/master/mjpg-streamer-experimental/plugins/input_raspicam/README.md

Once the tool is running you can access your Raspberry Pi hostname/IP address
port 8080 in a browser to see the video.  For example access: http://raspberrypi:8080/
Or to access the stream directly (like to embed in a webpage) access: http://raspberrypi:8080/?action=stream

## systemd Service

Finally to make the mjpeg-streamer tool always run when the Pi boots you can create
and use a small systemd service.  The included mjpeg-streamer.service file is this
systemd service and you can install it by running the following commands from inside
the same directory as this README.md file.

First you will want to replace the start.sh shell script included with mjpeg-streamer
with a simpler script that uses the Pi camera plugin (just like manually running it
above).  The included start.sh file can be used to replace the script by running:

    cp start.sh /home/pi/mjpg-streamer/mjpg-streamer-experimental/
    chmod a+x /home/pi/mjpg-streamer/mjpg-streamer-experimental/start.sh

If you need to make any changes to how the Pi camera plugin is invoked (like the
vertical flip option, FPS, etc) be sure to change the start.sh script appropriately.

Then copy the systemd service to the location of all services by running:

    sudo cp mjpeg-streamer.service /lib/systemd/services/

Now have systemd reload its services by running:

    sudo systemctl daemon-reload

And enable the new service so it starts on boot by running:

    sudo systemctl enable mjpeg-streamer.service

Finally you can manually start the service by running:

    sudo systemctl start mjpeg-streamer.service

You can check the status of the service with the command:

    sudo systemctl status mjpeg-streamer.service

You should see the service is up and running without any errors.  If there are errors
carefully check the start.sh shell script is in the right location (the _exact_ path
specified in the copy command above) and it has the right options to invoke the Pi
camera plugin (try running the shell script yourself to confirm).

Now whenever the Pi boots the mjpeg-streamer service should automatically run and
start serving video of the Pi camera.
