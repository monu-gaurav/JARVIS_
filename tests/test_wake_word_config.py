"""Regression tests for the legacy wake-word setting migration."""
import json
import tempfile
import unittest
from pathlib import Path

import memory.config_manager as config_manager


class WakeWordConfigMigrationTests(unittest.TestCase):
    def setUp(self):
        self._old_dir = config_manager.CONFIG_DIR
        self._old_file = config_manager.CONFIG_FILE
        self._temp = tempfile.TemporaryDirectory()
        config_manager.CONFIG_DIR = Path(self._temp.name)
        config_manager.CONFIG_FILE = config_manager.CONFIG_DIR / "api_keys.json"

    def tearDown(self):
        config_manager.CONFIG_DIR = self._old_dir
        config_manager.CONFIG_FILE = self._old_file
        self._temp.cleanup()

    def _write_config(self, data):
        config_manager.CONFIG_FILE.write_text(json.dumps(data), encoding="utf-8")

    def test_legacy_auto_disabled_value_migrates_to_enabled(self):
        self._write_config({"wake_word_enabled": False})
        self.assertTrue(config_manager.get_wake_word_enabled())
        saved = json.loads(config_manager.CONFIG_FILE.read_text(encoding="utf-8"))
        self.assertTrue(saved["wake_word_enabled"])
        self.assertEqual(saved["wake_word_setting_version"], 2)

    def test_explicit_current_setting_can_remain_disabled(self):
        self._write_config({"wake_word_enabled": False, "wake_word_setting_version": 2})
        self.assertFalse(config_manager.get_wake_word_enabled())


if __name__ == "__main__":
    unittest.main()
