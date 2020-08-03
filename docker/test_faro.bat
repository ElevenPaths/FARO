@ECHO off
ECHO Running FARO tests...
REM Get container reference environment variable or set default
IF "%FARO_CONTAINER%"=="" (
    set FARO_CONTAINER="docker_faro-server_1"
)
REM Get faro source code folder relative to the location of this script
IF "%REL_PATH_SCRIPT_FARO_SRC%"=="" (
    set REL_PATH_SCRIPT_FARO_SRC="..\"
)
PUSHD %~dp0%REL_PATH_SCRIPT_FARO_SRC%
SET FARO_PATH=%CD%
POPD

IF [%1]==[] (
    docker exec %FARO_CONTAINER% ./test-local.sh
) ELSE (
    REM Wait until --env-file for docker exec is released
    docker run --network faro-net --rm^
    --env-file "%1" ^
    -v "%FARO_PATH%":/faro-project ^
    faro:latest ^
    ./test-local.sh
)
