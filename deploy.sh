#!/bin/bash

# Stop currently running container
docker stop $(docker ps -f ancestor=dolphinfeeds -q)

# Remove stopped containers
docker container prune -f

# Purge old images if exist
docker image rm dolphinfeeds

# Build image
docker build -t dolphinfeeds .

# Run in detached mode
docker run -d dolphinfeeds