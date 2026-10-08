#!/bin/bash
# Install the theme's Quickshell bar and its theme-switch integration once.
set -euo pipefail

theme_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
config_dir="$HOME/.config/omarchy"
state_dir="$HOME/.local/state/omarchy/orbita-bar"
plugin_dir="$config_dir/plugins/orbita.bar"

for required_command in jq omarchy omarchy-shell flock; do
  command -v "$required_command" >/dev/null || {
    echo "Required command not found: $required_command" >&2
    exit 1
  }
done

if [[ -d $plugin_dir ]]; then
  mkdir -p "$state_dir/backups"
  backup_dir=$(mktemp -d "$state_dir/backups/bar.XXXXXX")
  cp -a "$plugin_dir/." "$backup_dir/"
fi
mkdir -p "$plugin_dir"
cp -a "$theme_dir/integrations/plugins/orbita.bar/." "$plugin_dir/"
omarchy hook install theme-set "$theme_dir/integrations/orbita-bar"
omarchy-shell -q shell rescanPlugins >/dev/null 2>&1 || true

current_theme=""
if [[ -f $HOME/.local/state/omarchy/current/theme.name ]]; then
  current_theme=$(cat "$HOME/.local/state/omarchy/current/theme.name")
fi
bash "$config_dir/hooks/theme-set.d/orbita-bar" "$current_theme"
echo "Órbita floating bar installed. It activates when Órbita is selected."
