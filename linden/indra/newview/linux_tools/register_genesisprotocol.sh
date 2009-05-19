#!/bin/bash

# Register a protocol handler (default: handle_genesisprotocol.sh) for
# URLs of the form genesis://...
#

HANDLER="$1"

RUN_PATH=`dirname "$0" || echo .`
cd "${RUN_PATH}"

if [ -z "$HANDLER" ]; then
    HANDLER=`pwd`/handle_genesisprotocol.sh
fi

# Register handler for GNOME-aware apps
LLGCONFTOOL2=gconftool-2
if which ${LLGCONFTOOL2} >/dev/null; then
    (${LLGCONFTOOL2} -s -t string /desktop/gnome/url-handlers/genesis/command "${HANDLER} \"%s\"" && ${LLGCONFTOOL2} -s -t bool /desktop/gnome/url-handlers/genesis/enabled true) || echo Warning: Did not register genesis:// handler with GNOME: ${LLGCONFTOOL2} failed.
else
    echo Warning: Did not register genesis:// handler with GNOME: ${LLGCONFTOOL2} not found.
fi

# Register handler for KDE-aware apps
if [ -z "$KDEHOME" ]; then
    KDEHOME=~/.kde
fi
LLKDEPROTDIR=${KDEHOME}/share/services
if [ -d "$LLKDEPROTDIR" ]; then
    LLKDEPROTFILE=${LLKDEPROTDIR}/genesis.protocol
    cat > ${LLKDEPROTFILE} <<EOF || echo Warning: Did not register genesis:// handler with KDE: Could not write ${LLKDEPROTFILE}
[Protocol]
exec=${HANDLER} '%u'
protocol=genesis
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF
else
    echo Warning: Did not register genesis:// handler with KDE: Directory $LLKDEPROTDIR does not exist.
fi
