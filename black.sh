#!/bin/bash

docker build . -f Dockerfile.black -t black
docker run -it --rm -v $(pwd)/bot:/bot black
docker run -it --rm -v $(pwd)/bot:/bot black pylint --disable=R,C,W1203,W0105 bot/main.py
