#!/usr/bin/env bash

docker run -v /tmp/.X11-unix:/tmp/.X11-unix -v ${PWD}/results:/home/physicist/results --rm -it --user $(id -u) -p 8888:8888 $1
