#!/bin/bash

# Send a URL of the form genesis://... to the viewer.
#

URL="$1"

if [ -z "$URL" ]; then
    echo Usage: $0 genesis://...
    exit
fi

RUN_PATH=`dirname "$0" || echo .`
cd "${RUN_PATH}"

exec ./heritage_key -genesis \'"${URL}"\'

