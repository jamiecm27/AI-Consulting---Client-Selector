#!/bin/bash
HERE="$(cd "$(dirname "$0")" && pwd)"
/bin/bash "$HERE/_mac_run.sh" start
RESULT=$?
if [ "$RESULT" -ne 0 ]; then
    printf '\nPlease copy the error above into the ChatGPT conversation.\n'
fi
printf '\nPress Return to close this window.\n'
read -r _unused
exit "$RESULT"
