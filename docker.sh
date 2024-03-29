#!/bin/bash

ADMIN_COMMAND="sudo"                                # Use doas if you are a chad
IMAGE_NAME="discord-bot"                            # Image and container name for docker
MOUNT_FLAGS="-v $(pwd):/discord-bot"                # Flag for specifying the folder mount point (so logs and configs persist)
ENVIROMENT_FLAGS="-e PYTHONDONTWRITEBYTECODE=1"     # Flag for enviroment variables
DOCKER_RUN_FLAGS="--rm -it -d --name $IMAGE_NAME"   # Flags for ./docker.sh run

# First check if there are no arguments
if [[ $# == 0 ]]; then
    echo "No arguments detected! Use './docker.sh --help' to see the help!"
    echo "Exiting..."
    exit 1;
fi

# Check the commands that will only be executed once, in this case help
if [[ " $* " == *" help "* || " $* " == *" --help "* ]]; then
    echo "Showing help for docker.sh"
    echo "  ./docker.sh help    | Show this help"
    echo "  ./docker.sh stop    | Stop the docker container ($IMAGE_NAME)"
    echo "  ./docker.sh clean   | Remove the docker image (The container is auto-removed by default)"
    echo "  ./docker.sh build   | Build the docker container ($IMAGE_NAME:latest)"
    echo "  ./docker.sh run     | Run the docker container ($IMAGE_NAME:latest)"
    exit 1;
fi

# Check arguments that can be convined. They are in this order because you 
# never want to stop the container on the same command you start it.
if [[ " $* " == *" stop "* ]]; then
    echo "$ADMIN_COMMAND docker stop $IMAGE_NAME"
    $ADMIN_COMMAND docker stop $IMAGE_NAME
fi
if [[ " $* " == *" clean "* || " $* " == *" clear "* ]]; then
    echo "$ADMIN_COMMAND docker rmi $IMAGE_NAME:latest"
    $ADMIN_COMMAND docker rmi $IMAGE_NAME:latest
fi
if [[ " $* " == *" build "* ]]; then
    echo "$ADMIN_COMMAND docker build -t $IMAGE_NAME:latest ."
    $ADMIN_COMMAND docker build -t $IMAGE_NAME:latest .
fi
if [[ " $* " == *" run "* ]]; then
    echo "$ADMIN_COMMAND docker run $DOCKER_RUN_FLAGS $ENVIROMENT_FLAGS $MOUNT_FLAGS $IMAGE_NAME"
    $ADMIN_COMMAND docker run $DOCKER_RUN_FLAGS $ENVIROMENT_FLAGS $MOUNT_FLAGS $IMAGE_NAME
fi

