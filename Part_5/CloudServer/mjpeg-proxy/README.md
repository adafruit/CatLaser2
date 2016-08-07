# mjpeg-proxy setup

To install mjpeg-proxy on the Ubuntu 16.04 cloud server you'll want to run the
following commands.

First install NodeJS and NPM with these commands:

    sudo apt-get update
    sudo apt-get install -y nodejs nodejs-legacy npm

Now create a new folder to contain the mjpeg-proxy code and bootstrap code to
start its server process:

    cd ~
    mkdir mjpeg-proxy
    npm install mjpeg-proxy express

Inside that folder you'll need to copy in the mjpeg-proxy.js file in this directory.
Modify the file so the configuration variables at the top match your setup (like
the videoSource path to the MJPEG stream on your Pi).  Then run the tool by
invoking in the directory:

    node mjpeg-proxy.js

Once the tool is running you should see no output.  Open a browser and point it at
the cloud server IP address (if running in a Vagrant VM you might need to forward
a local port on the host machine to port 8080 on the cloud server virtual machine--the
Vagrantfile for this project is already configured for this).  For example with the
VM running on the same machine as the browser access:

    http://localhost:8080/index1.jpg

You should see the proxied video stream.  If you open multiple browser tabs to this
video stream it will still only make one connection to the Raspberry Pi!
