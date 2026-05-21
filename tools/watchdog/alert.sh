#!/usr/bin/env bash
# alert.sh — write/append an alert line to ALERT.txt for a service state transition.
#
# Args: <service> <url> <new_status> <prev_status>
#   new_status:  UP | DOWN
#   prev_status: UP | DOWN | UNKNOWN
#
# UP -> DOWN     => ALERT line
# DOWN -> UP     => RECOVERED line
# UNKNOWN -> *   => INIT line (first sighting; logged but not screaming)

set -u

if [[ $# -lt 4 ]]; then
  echo "usage: $0 <service> <url> <new_status> <prev_status>" >&2
  exit 2
fi

SERVICE="$1"
URL="$2"
NEW="$3"
PREV="$4"

PREVIEW_DIR="${NEXOURA_PREVIEW_DIR:-/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview}"
ALERT="$PREVIEW_DIR/ALERT.txt"
mkdir -p "$PREVIEW_DIR"

ts="$(date -Iseconds)"

case "${PREV}_${NEW}" in
  UP_DOWN)      kind="ALERT" ;;
  DOWN_UP)      kind="RECOVERED" ;;
  UNKNOWN_DOWN) kind="INIT-DOWN" ;;
  UNKNOWN_UP)   kind="INIT-UP" ;;
  *)            kind="STATE" ;;
esac

echo "$ts $kind $SERVICE $URL (prev=$PREV new=$NEW)" >> "$ALERT"
