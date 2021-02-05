#!/bin/bash
echo "Testing FARO..."

# Check whether TIKA_SERVER_ENDPOINT is set, if not set based on TIKA_PORT
if [ -z "${TIKA_SERVER_ENDPOINT}" ]
then
  TIKA_PORT=${TIKA_PORT:-9998}
  export TIKA_SERVER_ENDPOINT="http://tika-server:$TIKA_PORT/"
fi

cd /faro-project
# Use dockerize since depends_on condition has been removed from docker-compose
# more info: https://github.com/jwilder/dockerize
dockerize -wait "$TIKA_SERVER_ENDPOINT/tika" -timeout 10s
if [ $? -ne 0 ]
then
  echo "Error: Looks like tika server is unreachable"
  exit 1
fi
nosetests -sv ./test/test_*.py --with-coverage --cover-package=faro
