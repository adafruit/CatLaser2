// mjpeg-proxy bootstrap code
// This will run a small webserver on port 8080 that serves up the Pi's video
// stream on the path /index1.jpg.  Make sure to modify the videoSource URL
// variable so that it points to the URL of the MJPEG stream from your Pi.

// Configuration:
var videoSource = 'http://raspberrypi:8080/?action=stream';  // Path to the source
                                                             // MJPEG stream on the Pi.
var port        = 8080;           // Port for the webserver this tool creates.
var path        = '/index1.jpg';  // The path to the MJPEG stream that will be
                                  // served by this tool.
// Setup MjpegProxy instance and basic express webapp.
var MjpegProxy = require('mjpeg-proxy').MjpegProxy;
var express = require('express');
var app = express();

// Define route for the proxied MJPEG stream and start listening.
app.get(path, new MjpegProxy(videoSource).proxyRequest);
app.listen(port);
