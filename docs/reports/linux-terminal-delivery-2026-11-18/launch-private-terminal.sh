#!/usr/bin/env bash
# Opt-in launcher; preparing this file does not start a terminal.
# Usage: launch-private-terminal.sh COMMAND [ARG...]
set -euo pipefail
launcher_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ ${1:-} == --check ]]; then
  for setting in menu-accelerator-enabled shortcuts-enabled mnemonics-enabled always-check-default-terminal; do
    printf '%s=' "$setting"
    env GSETTINGS_BACKEND=keyfile XDG_CONFIG_HOME="$launcher_dir/private-config" \
      gsettings get org.gnome.Terminal.Legacy.Settings "$setting"
  done
  exit 0
fi
if (( $# == 0 )); then
  printf 'Usage: %s COMMAND [ARG...]\n' "$0" >&2
  exit 2
fi
instance_dir=$(mktemp -d /tmp/wordling-terminal-instance.XXXXXX)
mkdir -p -- "$instance_dir/config/glib-2.0/settings"
cp -- "$launcher_dir/private-config/glib-2.0/settings/keyfile" \
  "$instance_dir/config/glib-2.0/settings/keyfile"
app_id="org.wordling.KeyboardCheck.p$$"
server_pid=''
cleanup() {
  if [[ -n "$server_pid" ]]; then
    kill "$server_pid" 2>/dev/null || true
    # Give this server one second to exit, then prevent TERM-resistant cleanup
    # from keeping the launcher alive indefinitely.
    for (( cleanup_attempt=0; cleanup_attempt<20; cleanup_attempt++ )); do
      if ! kill -0 "$server_pid" 2>/dev/null; then
        break
      fi
      sleep 0.05
    done
    if kill -0 "$server_pid" 2>/dev/null; then
      kill -KILL "$server_pid" 2>/dev/null || true
    fi
    wait "$server_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf 'Private terminal instance: %s\n' "$instance_dir" >&2
# Scope these settings to the newly spawned server. The client and its child
# retain the caller's original environment, including application config paths.
env GSETTINGS_BACKEND=keyfile XDG_CONFIG_HOME="$instance_dir/config" \
  /usr/libexec/gnome-terminal-server --app-id "$app_id" \
  --class WordlingKeyboardCheck >"$instance_dir/server.log" 2>&1 &
server_pid=$!
ready=false
readiness_deadline=$((SECONDS + 10))
while (( SECONDS < readiness_deadline )); do
  if timeout --kill-after=0.2s 1s gdbus call --session --dest org.freedesktop.DBus \
      --object-path /org/freedesktop/DBus \
      --method org.freedesktop.DBus.NameHasOwner "$app_id" 2>/dev/null | \
      rg -q '^\(true,\)$'; then
    ready=true
    break
  fi
  if ! kill -0 "$server_pid" 2>/dev/null; then
    printf 'Private terminal server exited; inspect %s/server.log\n' "$instance_dir" >&2
    exit 1
  fi
  sleep 0.1
done
if [[ "$ready" != true ]]; then
  printf 'Private terminal server did not register; inspect %s/server.log\n' "$instance_dir" >&2
  exit 1
fi
/usr/bin/gnome-terminal.real --app-id "$app_id" --wait --hide-menubar \
  --title 'Wordling KeyboardCheck' -- "$@"
