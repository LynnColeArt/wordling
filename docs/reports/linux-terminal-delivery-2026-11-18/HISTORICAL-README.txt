Bounded private GNOME Terminal keyboard-check launcher

Artifacts:
- launch-private-terminal.sh: opt-in isolated-server launcher
- private-config/glib-2.0/settings/keyfile: four process-private settings
- proof.txt: original non-GUI backend/readback evidence
- final-non-gui-proof.txt: final launcher syntax/readbacks after bounded lifecycle edits
- root-gui-smoke-provenance.txt: root-reported successful /bin/true GUI smoke
- launch-private-terminal.smoke-tested.sh: exact original GUI-smoked launcher
- SHA256SUMS: final launcher, original launcher, config and proof hashes
- source snapshots in this directory: source-backed explanation only; not a checkout
- hid-apple.ko: read-only decompression of installed 7.0.0-42-generic driver

Non-GUI inspection:
  /tmp/wordling-terminal-private-investigation/launch-private-terminal.sh --check

GUI smoke command (root ran original launcher successfully; see provenance):
  /tmp/wordling-terminal-private-investigation/launch-private-terminal.sh /bin/true

Current-binary diagnostic command (requires root coordination; not run here):
  /tmp/wordling-terminal-private-investigation/launch-private-terminal.sh /tmp/wordling-linux-keys-f6cea1cc-dlsi4ix9/launch-keyboard-diagnostic.sh

The final launcher uses org.wordling.KeyboardCheck.p<PID> and title Wordling
KeyboardCheck, then invokes its matching real client with --wait. Readiness has
a 10-second deadline with each D-Bus query limited to 1 second (+0.2s kill grace),
so a final query can extend total readiness slightly beyond the deadline. Its
EXIT trap sends TERM to its own server, allows 1 second, then uses KILL if
needed and reaps that child. Application runtime itself is intentionally unbounded. Each invocation
creates /tmp/wordling-terminal-instance.XXXXXX with private config and server.log.
The GSETTINGS_BACKEND and XDG_CONFIG_HOME overrides apply ONLY to the server,
so Wordling receives the caller's application environment. No system/global
GSettings writes, keyboard/kernel modifications, repository edits or commits.

Compatibility evidence:
1. GNOME Terminal 3.52 server.cc creates terminal_app_new(..., nullptr), and
   terminal-app.cc:979-980 selects g_settings_backend_get_default(). Installed
   server dynamically imports g_settings_backend_get_default (strings/ldd).
2. GLib 2.80 gsettingsbackend.c:999-1022 selects the GSETTINGS_BACKEND override.
   gkeyfilesettingsbackend.c registers keyfile and computes the filename from
   g_get_user_config_dir()/glib-2.0/settings/keyfile. Installed GLib 2.80.0 emits
   GKeyfileSettingsBackend in the actual non-GUI readback (proof.txt).
3. Local installed org.gnome.Terminal.gschema.xml documents F10 menu access and
   the menu-accelerator-enabled/shortcuts-enabled switches. terminal-window.cc
   :1370-1378 removes gtk-menu-bar-accel when false; :2080 onward binds the
   shortcut setting to gtk-enable-accels.
4. /usr/bin/gnome-terminal is a distro Python wrapper. We bypass it with an
   explicitly owned /usr/libexec/gnome-terminal-server and /usr/bin/gnome-terminal.real.

Limitations:
- Source plus non-GUI readback verifies this is a valid isolated settings path.
  Root ran the original launcher with /bin/true: exit 0 in 0.37 seconds;
  no remaining owned server and global settings remained true. The final
  KeyboardCheck rename and bounded readiness/cleanup edits passed syntax and
  non-GUI settings readback only; no further GUI action was performed.
- Releasing terminal interception cannot release Cinnamon/window-manager global
  grabs or transform media-key events into function keys. Physical F5/F10 and
  Ctrl+F1 delivery remains unverified; physical trace has no function-key bytes.
- Existing real Linux PTY tests passed native F5/F10/Ctrl+F1 application actions.

Conservative hid_apple assessment:
- Sysfs confirms USB 05ac:024f, name HAILUCK CO.,LTD USB KEYBOARD, driver apple,
  current fnmode=3. Product 0x024f maps to APPLE_ALU_REVB_ANSI in upstream IDs.
- Upstream fnmode auto uses fkeyslast (1) unless a non-Apple or disabled-Fkeys
  quirk applies. Source's Hailuck prefix is case-sensitive and does not match
  the observed uppercase HAILUCK name. Installed module likewise contains
  Hailuck and apple_input_configured calls strncmp (module-proof.txt).
- This supports an Fn/media translation hypothesis, not proven physical cause.
  We have not captured kernel input events or the physical Fn+F5 result, and
  the upstream source snapshot is v6.19 rather than this exact distro kernel.
  No fnmode, driver binding, remapping or desktop preferences were changed.

Primary sources:
https://github.com/GNOME/gnome-terminal/blob/3.52.0/src/server.cc
https://github.com/GNOME/gnome-terminal/blob/3.52.0/src/terminal-app.cc
https://github.com/GNOME/gnome-terminal/blob/3.52.0/src/terminal-window.cc
https://github.com/GNOME/glib/blob/2.80.0/gio/gsettingsbackend.c
https://github.com/GNOME/glib/blob/2.80.0/gio/gkeyfilesettingsbackend.c
https://github.com/torvalds/linux/blob/v6.19/drivers/hid/hid-apple.c
https://github.com/torvalds/linux/blob/v6.19/drivers/hid/hid-ids.h
