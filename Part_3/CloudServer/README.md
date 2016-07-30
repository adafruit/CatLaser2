# Cloud Server Setup

This directory contains the Vagrant configuration file to get a basic cloud
server running as a virtual machine on your local computer.  Make sure to install
both the latest versions of Vagrant and VirtualBox (both free open source software)
before continuing.

Once the software is installed copy the Vagrantfile in this directory to a directory
on your PC.  Then in a terminal run the following command inside that directory:

    vagrant up

The first time this runs it will take some time as it downloads and sets up the VM.
Once Vagrant finishes running the VM will be active in the background.  Run the
following command to connect to the VM with SSH:

    vagrant ssh

This will connect you to the terminal of the Linux VM automatically.

To exit the VM run the following command:

    exit

Note that once you exit the VM is still running in the background!  To stop the
VM run the following command:

    vagrant halt

You can start the VM again by using the `vagrant up` command (the second time you
run the VM it will be much faster to start).

## MQTT Broker Setup

Once the VM is running you will want to setup a MQTT broker that will be used to
send laser control messages to the Pi.  The mosquitto MQTT broker will be used
for this as it is easy to setup and configure.  For now a basic configuration with
no authentication will be used, however it is advised that you explore how to secure
the server when using in a 'production' setting (later videos will cover this topic).

To install mosquitto run the following commands inside the cloud server VM:

    sudo apt-get update
    sudo apt-get install -y mosquitto mosquitto-clients

At this point mosquitto MQTT server will be setup and running with its default
configuration of port 1883 public access.  This configuration is fine for the needs
of this video.

However since the cloud server is running in a VM and the Raspberry Pi needs to
access it you will want to setup forwarding of port 1883 on the host machine (i.e.
the machine running the VM) to port 1883 of the guest machine (i.e. the Ubuntu
cloud server).  The Vagrantfile already specifies this, but as a reference this
line in the file is how this port mapping is achieved:

    config.vm.network "forwarded_port", guest: 1883, host: 1883

Notice in the file there is also a port forwarding for port 8080 from host to guest.
This is used by the mjpeg-proxy tool to proxy access to the camera stream.
