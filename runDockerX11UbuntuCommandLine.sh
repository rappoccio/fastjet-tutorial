#!/usr/bin/env bash

docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ${PWD}/results:/home/physicist/results --rm -it --user $(id -u) --entrypoint /bin/bash $1
