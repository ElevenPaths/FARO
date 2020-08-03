#!/bin/bash -e
if [ -z "$1" ]; then
    echo "enter at least one parameter"
    exit 2
fi
# points to faro source code relative to the location of this script
REL_PATH_SCRIPT_FARO_SRC=${REL_PATH_SCRIPT_FARO_SRC:-"../"}
# Get faro source code folder relative to the location of this script
pushd $(dirname "${BASH_SOURCE[0]}") > /dev/null
cd $REL_PATH_SCRIPT_FARO_SRC
FARO_PATH=$(pwd -P)
popd > /dev/null

echo "Analyzing documents..."
# Create output inside FARO_PATH
pushd $FARO_PATH > /dev/null
mkdir -p output
popd > /dev/null
INPUT_PATH=$(cd "$1"; pwd -P )
if [ -z "$2" ]; then
    docker run --network faro-net --rm \
        -v "$INPUT_PATH":/faro-project/input \
        -v "$FARO_PATH"/output:/faro-project/output \
        -v "$FARO_PATH":/faro-project \
        faro:latest ./entrypoint.sh input "$INPUT_PATH"
else
    docker run --network faro-net --env-file "$2" --rm \
        -v "$INPUT_PATH":/faro-project/input \
        -v "$FARO_PATH"/output:/faro-project/output \
        -v "$FARO_PATH":/faro-project \
        faro:latest ./entrypoint.sh input "$INPUT_PATH"
fi
