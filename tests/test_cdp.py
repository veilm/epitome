from types import SimpleNamespace
import unittest
from unittest.mock import patch

from util.epitome_lib import cdp


class CdpTest(unittest.TestCase):
    def test_close_session_tab_retries_transient_failure(self):
        with patch.object(
            cdp,
            "run",
            side_effect=[SimpleNamespace(returncode=1), SimpleNamespace(returncode=0)],
        ) as run:
            self.assertTrue(cdp.close_session_tab("capture", attempts=3))
        self.assertEqual(run.call_count, 2)

    def test_close_session_tab_returns_false_after_all_attempts(self):
        with patch.object(
            cdp,
            "run",
            return_value=SimpleNamespace(returncode=1),
        ) as run:
            self.assertFalse(cdp.close_session_tab("capture", attempts=3))
        self.assertEqual(run.call_count, 3)


if __name__ == "__main__":
    unittest.main()
