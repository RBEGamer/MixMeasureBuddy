#!/bin/bash
cd "$(dirname "$0")"


#!/bin/bash
IMAGE=docker.io/library/mixmeasurebuddyfirmwarebuilder
if [[ "$(docker images -q $IMAGE 2> /dev/null)" == "" ]]; then
  echo "$IMAGE IMAGE BUILD STARTED"
  docker build -t $IMAGE .
else
 echo "IMAGE $IMAGE EXISTS; NO BUILD REQUIRED"
fi

docker run -i --rm -v "$PWD:/var/build/src" $IMAGE