"""Exercise theme switching in isolated XDG directories, without a desktop."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HOOK = Path(__file__).resolve().parents[1] / "integrations" / "orbita-bar"


class BarHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / "config" / "omarchy" / "shell.json"
        self.config.parent.mkdir(parents=True)
        self.previous = self.root / "state" / "omarchy" / "orbita-bar" / "previous.json"
        self.manifest = self.config.parent / "plugins" / "orbita.bar" / "manifest.json"
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text('{}')
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        ipc = bin_dir / "omarchy-shell"
        ipc.write_text('#!/bin/sh\nexit 0\n')
        ipc.chmod(0o755)
        self.env = dict(os.environ,
                        XDG_CONFIG_HOME=str(self.root / "config"),
                        XDG_STATE_HOME=str(self.root / "state"),
                        OMARCHY_PATH=str(self.root / "omarchy"),
                        PATH=str(bin_dir) + os.pathsep + os.environ["PATH"])
        self.original = {
            "version": 1,
            "bar": {"id": "custom.bar", "position": "bottom", "transparent": True,
                    "centerAnchor": "custom.clock",
                    "layout": {"center": [{"id": "custom.clock", "format": "HH:mm"}]}},
            "idle": {"lock": 3600},
            "plugins": [{"id": "custom.notifications"}],
        }
        self.write(self.original)

    def write(self, value):
        self.config.write_text(json.dumps(value))

    def read(self):
        return json.loads(self.config.read_text())

    def run_hook(self, theme, success=True):
        result = subprocess.run(["bash", str(HOOK), theme], env=self.env,
                                capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)

    def test_activation_preserves_widgets_and_unrelated_settings(self):
        self.run_hook("orbita")
        actual = self.read()
        expected = json.loads(json.dumps(self.original))
        expected["bar"].update(id="orbita.bar", position="top", transparent=False)
        self.assertEqual(actual, expected)

    def test_repeated_activation_restores_original_and_keeps_widget_edits(self):
        self.run_hook("orbita")
        self.run_hook("orbita")
        modified = self.read()
        modified["bar"]["layout"]["center"].append({"id": "custom.weather"})
        self.write(modified)
        self.run_hook("catppuccin")
        expected = json.loads(json.dumps(self.original))
        expected["bar"]["layout"] = modified["bar"]["layout"]
        self.assertEqual(self.read(), expected)
        self.assertFalse(self.previous.exists())

    def test_restoration_removes_keys_that_were_originally_absent(self):
        for key in ("id", "position", "transparent"):
            del self.original["bar"][key]
        self.write(self.original)
        self.run_hook("orbita")
        self.run_hook("tokyo-night")
        self.assertEqual(self.read(), self.original)

    def test_manual_bar_selection_is_respected_on_departure(self):
        self.run_hook("orbita")
        modified = self.read()
        modified["bar"].update(id="different.bar", position="left")
        self.write(modified)
        self.run_hook("catppuccin")
        self.assertEqual(self.read(), modified)
        self.assertFalse(self.previous.exists())

    def test_other_theme_without_snapshot_does_nothing(self):
        before = self.config.read_bytes()
        self.run_hook("catppuccin")
        self.assertEqual(self.config.read_bytes(), before)
        self.assertFalse(self.previous.parent.exists())

    def test_fresh_install_uses_omarchy_defaults(self):
        self.config.unlink()
        defaults = self.root / "omarchy" / "config" / "omarchy" / "shell.json"
        defaults.parent.mkdir(parents=True)
        defaults.write_text(json.dumps(self.original))
        self.run_hook("orbita")
        self.assertEqual(self.read()["bar"]["layout"], self.original["bar"]["layout"])
        self.run_hook("catppuccin")
        self.assertEqual(self.read(), self.original)

    def test_missing_plugin_keeps_configuration(self):
        self.manifest.unlink()
        before = self.config.read_bytes()
        self.run_hook("orbita", success=False)
        self.assertEqual(self.config.read_bytes(), before)
        self.assertFalse(self.previous.exists())

    def test_malformed_config_is_not_overwritten(self):
        self.config.write_text('{broken')
        self.run_hook("orbita", success=False)
        self.assertEqual(self.config.read_text(), '{broken')
        self.assertFalse(self.previous.exists())


if __name__ == "__main__":
    unittest.main()
