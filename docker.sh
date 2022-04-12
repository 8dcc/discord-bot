#!/bin/bash

ADMIN_COMMAND="sudo"                                # Use doas if you are a chad
IMAGE_NAME="discord-bot"                            # Image and container name for docker
DOCKER_RUN_FLAGS="--rm -it -d --name $IMAGE_NAME"   # Flags for ./docker.sh run

if [[ $1 == "clean" || $1 == "clear" ]]; then
    $ADMIN_COMMAND docker rmi $IMAGE_NAME:latest
elif [[ $1 == "build" ]]; then
    $ADMIN_COMMAND docker build -t $IMAGE_NAME:latest .
elif [[ $1 == "run" ]]; then
    $ADMIN_COMMAND docker run $DOCKER_RUN_FLAGS $IMAGE_NAME
elif [[ $1 == "stop" ]]; then
    $ADMIN_COMMAND docker stop $IMAGE_NAME
elif [[ $1 == "help" || $1 == "--help" ]]; then
    echo "Showing help for docker.sh"
    echo "  ./docker.sh help    | Show this help"
    echo "  ./docker.sh build   | Build the docker container (discord-bot:latest)"
    echo "  ./docker.sh run     | Run the docker container (discord-bot:latest)"
else
    echo "No argument detected! Use './docker.sh --help' to see the help!"
    echo "Exiting..."
    exit 1;
fi
