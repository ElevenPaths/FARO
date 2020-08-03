#!/bin/bash -e
cd /faro-project
SUFFIX=$(date "+%Y.%m.%d-%H.%M.%S")

# Check whether TIKA_SERVER_ENDPOINT is set, if not set based on TIKA_PORT
if [ -z "${TIKA_SERVER_ENDPOINT}" ]
then
  TIKA_PORT=${TIKA_PORT:-9998}
  export TIKA_SERVER_ENDPOINT="http://tika-server:$TIKA_PORT/"
fi


if [ -z "$1" ]
then
  echo "Hello FARO"
else
  ./faro_spider.sh $1 $SUFFIX
  # Get the path inside docker container
  DOCKER_PATH="/faro-project/$1"
  # Replace path inside docker to host path for the end-user
  PREFIX=$(echo $2 | sed -e 's/\\/\\\\/g; s/\//\\\//g; s/&/\\\&/g')
  if [[ -z "$3" || "$3" != "win" ]]
  then
  	# UNIX
     	sed -i.bak "s|$DOCKER_PATH|$PREFIX|" output/scan.$SUFFIX.csv
     	sed -i.bak "s|$DOCKER_PATH|$PREFIX|" output/scan.$SUFFIX.entity
  else
  	# Windows
     	sed -i.bak "s|$DOCKER_PATH|$PREFIX| ; s|/|\\\\|g ; s|,application\\\\|,application\/| ; s|,text\\\\|,text\/|" output/scan.$SUFFIX.csv
     	sed -i.bak "s|$DOCKER_PATH|$PREFIX| ; s|/|\\\\|g ; s|,application\\\\|,application\/|" output/scan.$SUFFIX.entity
  fi

  # Clean backup files
  rm output/scan.$SUFFIX.csv.bak
  rm output/scan.$SUFFIX.entity.bak
fi
