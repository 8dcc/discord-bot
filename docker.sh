#!/bin/bash

ADMIN_COMMAND="sudo"            # Use doas if you are a chad
DOCKER_RUN_FLAGS="--rm -it -d --name discord-bot"  # Flags for ./docker.sh run

if [[ $1 == "build" ]]; then
    $ADMIN_COMMAND docker build -t discord-bot:latest .
elif [[ $1 == "run" ]]; then
    $ADMIN_COMMAND docker run $DOCKER_RUN_FLAGS discord-bot
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
