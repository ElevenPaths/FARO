@ECHO off
IF [%1]==[] (
    ECHO "enter at least one parameter"
    EXIT /B 2
)
REM Get the folder with faro source code relative to the location of this script to be able to mount faro source code volume
IF "%REL_PATH_SCRIPT_FARO_SRC%"=="" (
    set REL_PATH_SCRIPT_FARO_SRC="..\"
)
ECHO Analyzing documents...
REM get path relative to the current script location
PUSHD %1
SET INPUT_PATH=%CD%
POPD
REM get faro path starting from script location
PUSHD %~dp0%REL_PATH_SCRIPT_FARO_SRC%
SET FARO_PATH=%CD%
IF NOT EXIST output MKDIR output
POPD

IF [%2]==[] (
    docker run --network faro-net --rm ^
    -v "%FARO_PATH%":/faro-project ^
    -v "%INPUT_PATH%":/faro-project/input ^
    -v "%FARO_PATH%"\output:/faro-project/output ^
    faro:latest ./entrypoint.sh input "%INPUT_PATH%" win
) ELSE (
    docker run --network faro-net --env-file "%2" --rm ^
    -v "%FARO_PATH%":/faro-project ^
    -v "%INPUT_PATH%":/faro-project/input ^
    -v "%FARO_PATH%"\output:/faro-project/output ^
    faro:latest ./entrypoint.sh input "%INPUT_PATH%" win
)
