#!/bin/bash -e
java -Dlog4j.configuration=file:/log4j.properties -jar /tika-server-${TIKA_VERSION}.jar -h 0.0.0.0 -p ${TIKA_PORT}
