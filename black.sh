#!/bin/bash

docker build . -f Dockerfile.black -t black
docker run -it --rm -v $(pwd)/bot:/bot black black /bot