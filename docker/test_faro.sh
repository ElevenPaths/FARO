#!/bin/bash
echo "Running FARO tests..."
# we do this until the new work on docker-exec --env-file is released
# merged in master branch https://github.com/docker/cli/issues/1681 expected in next release
function generate_env
{
    INLINE_ENV=$(grep -v -E '^(#.*|[[:space:]]*|.*=\s*)$' "$1" | while read line; do echo "-e $line"; done)
    echo "$INLINE_ENV"
}

FARO_CONTAINER=${FARO_CONTAINER:-docker_faro-server_1}
if [ -z "$1" ]; then
    docker exec $FARO_CONTAINER ./test-local.sh
else
    docker exec $(generate_env "$1") $FARO_CONTAINER ./test-local.sh
fi

