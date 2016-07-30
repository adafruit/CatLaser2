# Cat Laser Toy 2.0 Part 3

This part of the series explores how to separate the original cat laser code into
two parts, one that runs on the Raspberry Pi and controls the laser and another
that runs on a server (in this case an Ubuntu virtual machine running in Vagrant/VirtualBox)
to provide laser control for many users.  This video explores the following topics:

-   Using [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to easily setup a small
    Linux server that will act as the development server for the cloud half of the
    project.  Using a Linux VM gives a consistent and easy to setup environment
    for writing the server code.

-   Setting up [mjpeg-proxy](https://www.npmjs.com/package/mjpeg-proxy) as an
    intelligent MJPEG reverse proxy.  This tool allows a Raspberry Pi to serve
    a video stream of its camera to many users.  The tool runs on a cloud server
    and makes one connection to the Pi to read its camera MJPEG video stream,
    then broadcasts that video out to any connected user.

-   Using MQTT and a MQTT broker on the cloud server to control target of the
    laser toy.  This is an important step because it allows the Pi and its laser
    controller to run separately from the server.  When the server wants to control
    the laser it broadcasts a message on the MQTT broker which the Pi receives and
    uses to move the laser.

The following code is in this repository:

-   RaspberryPi/LaserDriver - This is the Python 3 code which runs on the Pi and connects
    to the cloud server's MQTT broker allowing remote control of the laser targeting.

-   RaspberryPi/LaserServer - This is the original cat laser project code and is used
    to calibrate the laser so that it can turn screen clicks into servo positions.
    Note that this is NOT the server users will access to control the laser!  Instead
    this is purely for admin/internal use.  Users will access the cloud server and
    special code it's running to control the laser.

-   RaspberryPi/mjpeg-streamer - Instructions and a systemd service to run the
    mjpeg-streamer tool to serve a MJPEG video stream of the Pi camera.

-   CloudServer - This is a Vagrant configuration file for the cloud server.

-   CloudServer/mjpeg-proxy - Instructions on how to setup mjpeg-proxy on the
    cloud server so it can relay the Pi's video stream to multiple users.
