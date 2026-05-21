#!/usr/bin/env bash
# watchdog.sh — poll a list of local services and emit alerts on UP↔DOWN transitions.
#
# Reads services.yaml (sibling file), pings each service every $WATCHDOG_INTERVAL
# seconds (default 60), logs each check to $HOME/.hermes/watchdog.log, and calls
# alert.sh on state transitions (which appends to $NEXOURA_PREVIEW_DIR/ALERT.txt).
#
# Env overrides:
#   WATCHDOG_INTERVAL    polling interval in seconds (default 60)
#   WATCHDOG_CONF        path to services.yaml (default: sibling of this script)
#   WATCHDOG_LOG         path to log file (default: $HOME/.hermes/watchdog.log)
#   NEXOURA_PREVIEW_DIR  directory where ALERT.txt lives
#                        (default: /mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview)
#   WATCHDOG_ONCE=1      run a single iteration and exit (used by tests)

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="${WATCHDOG_CONF:-$SCRIPT_DIR/services.yaml}"
LOG="${WATCHDOG_LOG:-$HOME/.hermes/watchdog.log}"
PREVIEW_DIR="${NEXOURA_PREVIEW_DIR:-/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview}"
ALERT_SCRIPT="$SCRIPT_DIR/alert.sh"
INTERVAL="${WATCHDOG_INTERVAL:-60}"

mkdir -p "$(dirname "$LOG")" "$PREVIEW_DIR"

if [[ ! -f "$CONF" ]]; then
  echo "watchdog: config not found at $CONF" >&2
  exit 1
fi

# ---- parse services.yaml into parallel arrays NAME / URL / FBURL ----
NAME=()
URL=()
FBURL=()

parse_with_yq() {
  local count i
  count=$(yq '.services | length' "$CONF")
  for ((i=0; i<count; i++)); do
    NAME+=("$(yq -r ".services[$i].name" "$CONF")")
    URL+=("$(yq -r ".services[$i].url" "$CONF")")
    local fb
    fb=$(yq -r ".services[$i].fallback_url // \"\"" "$CONF")
    FBURL+=("$fb")
  done
}

parse_with_grep() {
  # Flat YAML parser: walk lines, accumulate fields per `- name:` block.
  local cur_name="" cur_url="" cur_fb=""
  flush() {
    if [[ -n "$cur_name" ]]; then
      NAME+=("$cur_name")
      URL+=("$cur_url")
      FBURL+=("$cur_fb")
    fi
    cur_name=""; cur_url=""; cur_fb=""
  }
  while IFS= read -r line; do
    # strip comments and trailing whitespace
    line="${line%%#*}"
    line="${line%"${line##*[![:space:]]}"}"
    [[ -z "$line" ]] && continue
    if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*name:[[:space:]]*(.+)$ ]]; then
      flush
      cur_name="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]+url:[[:space:]]*(.+)$ ]]; then
      cur_url="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^[[:space:]]+fallback_url:[[:space:]]*(.+)$ ]]; then
      cur_fb="${BASH_REMATCH[1]}"
    fi
  done < "$CONF"
  flush
}

if command -v yq >/dev/null 2>&1; then
  parse_with_yq
else
  parse_with_grep
fi

if [[ ${#NAME[@]} -eq 0 ]]; then
  echo "watchdog: no services parsed from $CONF" >&2
  exit 1
fi

echo "watchdog: monitoring ${#NAME[@]} service(s); log=$LOG interval=${INTERVAL}s" >&2

check_one() {
  local url="$1" out
  # -s silent, --max-time bound. We deliberately do NOT use -f because we want
  # the HTTP code printed even on 4xx/5xx. On connection failure curl writes
  # "000" via -w and exits non-zero — fall back to literal 000 in that case.
  out=$(curl -s --max-time 5 -o /dev/null -w '%{http_code}' "$url" 2>/dev/null) || out=000
  [[ -z "$out" ]] && out=000
  echo "$out"
}

run_iteration() {
  local i code status prev prev_file
  for i in "${!NAME[@]}"; do
    code=$(check_one "${URL[i]}")
    if [[ ! "$code" =~ ^[23][0-9][0-9]$ ]] && [[ -n "${FBURL[i]:-}" ]]; then
      # try fallback url before declaring DOWN
      local fb_code
      fb_code=$(check_one "${FBURL[i]}")
      if [[ "$fb_code" =~ ^[23][0-9][0-9]$ ]]; then
        code="$fb_code"
      fi
    fi
    if [[ "$code" =~ ^[23][0-9][0-9]$ ]]; then status=UP; else status=DOWN; fi
    echo "$(date -Iseconds) ${NAME[i]} $status $code" >> "$LOG"

    prev_file="/tmp/watchdog-state-${NAME[i]}.txt"
    prev=$(cat "$prev_file" 2>/dev/null || echo UNKNOWN)
    if [[ "$prev" != "$status" ]]; then
      if [[ -x "$ALERT_SCRIPT" ]]; then
        "$ALERT_SCRIPT" "${NAME[i]}" "${URL[i]}" "$status" "$prev" || true
      fi
    fi
    echo "$status" > "$prev_file"
  done
}

if [[ "${WATCHDOG_ONCE:-0}" == "1" ]]; then
  run_iteration
  exit 0
fi

trap 'echo "watchdog: stopping" >&2; exit 0' INT TERM

while true; do
  run_iteration
  sleep "$INTERVAL"
done
