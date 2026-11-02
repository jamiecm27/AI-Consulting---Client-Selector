#!/bin/bash
# No downloads, sudo, pip, shell profile changes, or Gatekeeper changes.
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
ACTION="${1:-start}"
TARGET="$HOME/Applications/JamieClientSelector"
if [ "$ACTION" != "install" ]; then
    if [ -f "$TARGET/.install-marker.json" ]; then
        ROOT="$TARGET"
    elif [ ! -f "$ROOT/.install-marker.json" ]; then
        printf '\nPlease run "00 INSTALL ON MAC.command" first.\n'
        exit 1
    fi
fi
PYTHON=""
valid_python() {
    [ -x "$1" ] || return 1
    case "$1" in /usr/bin/python3) return 1 ;; esac
    "$1" -c 'import sys, sqlite3, ssl, fcntl; assert sys.version_info >= (3, 11)' >/dev/null 2>&1
}
if [ -f "$ROOT/.python-path" ]; then
    CANDIDATE="$(cat "$ROOT/.python-path")"
    if valid_python "$CANDIDATE"; then PYTHON="$CANDIDATE"; fi
fi
if [ -z "$PYTHON" ]; then
    for VERSION in 3.13 3.14 3.15 3.12 3.11; do
        for CANDIDATE in "/Library/Frameworks/Python.framework/Versions/$VERSION/bin/python$VERSION" "/opt/homebrew/bin/python$VERSION" "/usr/local/bin/python$VERSION"; do
            if valid_python "$CANDIDATE"; then PYTHON="$CANDIDATE"; break 2; fi
        done
    done
fi
if [ -z "$PYTHON" ]; then
    for CANDIDATE in /opt/homebrew/bin/python3 /usr/local/bin/python3 "$(command -v python3 2>/dev/null || true)"; do
        if valid_python "$CANDIDATE"; then PYTHON="$CANDIDATE"; break; fi
    done
fi
if [ -z "$PYTHON" ]; then
    printf '\nPython 3.11 or newer was not found. Python 3.13 is the tested series.\n'
    printf 'Install the standard macOS Python package from the official page.\n'
    printf 'Also run "Install Certificates.command" in the installed Python folder.\n'
    printf 'Then double-click "00 INSTALL ON MAC.command" again.\n'
    if [ "$(uname -s)" = "Darwin" ]; then
        /usr/bin/open 'https://www.python.org/downloads/macos/'
    fi
    exit 1
fi
cd "$ROOT" || exit 1
export PYTHONDONTWRITEBYTECODE=1
if [ "$ACTION" = "install" ]; then
    exec "$PYTHON" "$ROOT/install_mac.py"
else
    exec "$PYTHON" "$ROOT/client_selector_manager.py" "$ACTION"
fi
