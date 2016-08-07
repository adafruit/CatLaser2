#!/bin/sh
# Shell script to start mjpeg-streamer.
export LD_LIBRARY_PATH="$(pwd)"
./mjpg_streamer -i "./input_raspicam.so -vf -fps 30" -o "./output_http.so -w ./www"
