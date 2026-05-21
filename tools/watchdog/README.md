# watchdog — local service health monitor

A tiny bash polling loop that pings the local NEXOURA services (gateway, dashboard,
workspace) on a fixed interval, writes a structured log of every check, and emits
human-readable alerts when a service transitions between UP and DOWN.

No daemons, no dependencies beyond `curl` and `bash`. Optional `yq` is used if
present, otherwise a built-in grep/regex parser handles the flat `services.yaml`.

## What it does

Every `WATCHDOG_INTERVAL` seconds (default 60) the script:

1. Reads `services.yaml` (sibling of `watchdog.sh`).
2. For each service: `curl -sf --max-time 5 -o /dev/null -w '%{http_code}' <url>`.
   HTTP 2xx/3xx = UP, anything else (including timeout / connection refused, which
   yield `000`) = DOWN. If a `fallback_url` is set and the primary check fails,
   the fallback is tried before declaring DOWN.
3. Appends one line per service to `~/.hermes/watchdog.log`:
   `<ISO8601> <service> <UP|DOWN> <http_code>`.
4. Compares against the previous state stored in `/tmp/watchdog-state-<service>.txt`.
   If the state changed, `alert.sh` is invoked which appends to
   `$NEXOURA_PREVIEW_DIR/ALERT.txt`:
   - `UP -> DOWN`     → `ALERT` line
   - `DOWN -> UP`     → `RECOVERED` line
   - `UNKNOWN -> *`   → `INIT-*` line (first sighting after startup)

## Install

```bash
chmod +x tools/watchdog/watchdog.sh tools/watchdog/alert.sh
```

That's it. No package install required on a stock Ubuntu/WSL box that already
has `curl`.

## Run modes

### Foreground (dev / smoke test)

```bash
./tools/watchdog/watchdog.sh
```

Ctrl-C to stop. Log streams to `~/.hermes/watchdog.log`.

### tmux / screen

```bash
tmux new -d -s watchdog './tools/watchdog/watchdog.sh'
tmux attach -t watchdog   # to view live, Ctrl-B then D to detach
```

### systemd user unit

See `watchdog.service.example`. Copy it to `~/.config/systemd/user/watchdog.service`,
edit the `ExecStart` path, then:

```bash
systemctl --user daemon-reload
systemctl --user enable --now watchdog.service
journalctl --user -u watchdog -f
```

### One-shot (for testing)

```bash
WATCHDOG_ONCE=1 ./tools/watchdog/watchdog.sh
```

Runs a single check pass and exits — useful for cron-style invocation or CI.

## Configuration

### services.yaml

Flat YAML, one block per service:

```yaml
services:
  - name: gateway
    url: http://127.0.0.1:8642/api/health
    fallback_url: http://127.0.0.1:8642/
  - name: dashboard
    url: http://127.0.0.1:9119
  - name: workspace
    url: http://localhost:3000
```

`fallback_url` is optional; only the primary `url` is required.

### Environment overrides

| Var                   | Default                                                | Purpose                          |
|-----------------------|--------------------------------------------------------|----------------------------------|
| `WATCHDOG_INTERVAL`   | `60`                                                   | Seconds between polling rounds.  |
| `WATCHDOG_CONF`       | sibling `services.yaml`                                | Alternate config path.           |
| `WATCHDOG_LOG`        | `$HOME/.hermes/watchdog.log`                           | Log file path.                   |
| `NEXOURA_PREVIEW_DIR` | `/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview`   | Where `ALERT.txt` is written.    |
| `WATCHDOG_ONCE`       | `0`                                                    | If `1`, run a single pass.       |

If you are not on Omar's WSL box, set `NEXOURA_PREVIEW_DIR` to somewhere
sensible (e.g. `~/nexoura-preview`).

## Locations

- Log: `~/.hermes/watchdog.log` (one line per service per check)
- Alerts: `$NEXOURA_PREVIEW_DIR/ALERT.txt`
- State: `/tmp/watchdog-state-<service>.txt` (one file per service; safe to delete)

## Future: auto-restart

v1 is observe-only. A natural follow-up is per-service restart hooks (e.g. a
`restart:` field in `services.yaml` pointing at a shell command, called after N
consecutive DOWN checks). This was intentionally left out of v1 because every
service in NEXOURA has different restart semantics (systemd unit, npm script,
Python module, manual) and a one-size-fits-all hook is a footgun. Reach for
this only once the watchdog has been running long enough to know which
services actually flap.
