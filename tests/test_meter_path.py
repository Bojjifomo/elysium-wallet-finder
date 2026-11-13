import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import rpc


class MeterPathTest(unittest.TestCase):
    def test_default_is_vendored_file(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("RPC_METER_PATH", None)
            p = rpc._meter_path()
        self.assertEqual(p.name, "rpcmeter.py")
        self.assertTrue(p.exists())

    def test_env_overrides_and_expands_home(self):
        with mock.patch.dict(os.environ, {"RPC_METER_PATH": "~/x/meter.py"}):
            p = rpc._meter_path()
        self.assertEqual(p, Path("~/x/meter.py").expanduser())

    def test_missing_file_is_noop(self):
        rpc._meter = None
        try:
            with mock.patch.dict(sys.modules):
                sys.modules.pop("rpc_meter", None)
                self._run_missing()
        finally:
            rpc._meter = None

    def _run_missing(self):
        try:
            with mock.patch.dict(os.environ, {"RPC_METER_PATH": "/nonexistent/meter.py"}):
                rpc._meter_hit("http://x")  # must not raise
            self.assertFalse(rpc._meter)
        finally:
            rpc._meter = None


if __name__ == "__main__":
    unittest.main()
