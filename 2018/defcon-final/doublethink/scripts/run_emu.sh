#!/bin/bash

GRN=$(tput setaf 6 2>/dev/null)
RST=$(tput sgr0 2>/dev/null)
RED=$(tput setaf 1 2>/dev/null)

set -e

PLATFORM=$1
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
PLATDIR=$SCRIPTDIR/../platforms/$PLATFORM
shift

if [ -z "$FLAG" ]
then
	FLAG=$1
	shift
fi

if [ -z "$SHELLCODE" ]
then
	SHELLCODE=$(cat $1 | base64)
fi

TMPDIR=$(mktemp -d)
trap 'echo "$GRN[**] Cleaning up...$RST"; rm -rf $TMPDIR' EXIT
cd $TMPDIR
chmod 711 .
echo "$FLAG" > flag
( echo -n "$SHELLCODE" | base64 -d; dd if=/dev/zero of=/dev/stdout bs=4096 count=1 2>/dev/null || true ) | head -c 4096 > shellcode

echo "$GRN[**] Running $PLATFORM...$RST"
script -q result -c "SCRIPTDIR=$SCRIPTDIR PLATDIR=$PLATDIR $PLATDIR/run ./flag ./shellcode" &
sleep 10 &
wait -n
# ( ( killall sleep; sudo killall -9 -u nobody; killall script ) || true ) 2>/dev/null


echo "$GRN[**] $PLATFORM shellcode terminated. Checking results.$RST"
cat result | tr 'A-Z' 'a-z' > results.lower
if grep -q ${FLAG,,} results.lower
then
	echo "$GRN[:)] FLAG GOTTEN!$RST"
	exit 0
else
	echo "$RED[:(] NO FLAG!$RST"
	exit 1
fi
