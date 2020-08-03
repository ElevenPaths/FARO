#!/bin/bash
PORT=${TIKA_PORT:-9998}
response=$(curl http://tika-server:$PORT/tika | grep -c "This is Tika Server")

return_code=0

if [ "$response" -ne 1 ];
then
	return_code=1
	echo "Cannot connect with Tika server in port $TIKA_PORT"
fi

exit $return_code
