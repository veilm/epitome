import importlib.machinery
import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "research" / "inventory_lesswrong_cdp"
LOADER = importlib.machinery.SourceFileLoader("inventory_lesswrong_cdp", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class LessWrongInventoryTest(unittest.TestCase):
    def test_normalizes_lesswrong_post_slug_to_stable_id(self):
        self.assertEqual(
            MODULE.canonical_post_url(
                "https://www.lesswrong.com/posts/Abc123xyz/a-title?commentId=1"
            ),
            "https://www.lesswrong.com/posts/Abc123xyz",
        )

    def test_normalizes_sequence_route_to_post_identity(self):
        self.assertEqual(
            MODULE.canonical_post_url(
                "https://www.lesswrong.com/s/sequence123/p/Abc123xyz"
            ),
            "https://www.lesswrong.com/posts/Abc123xyz",
        )

    def test_deduplicates_alignment_forum_mirror_on_lesswrong(self):
        self.assertEqual(
            MODULE.canonical_post_url(
                "https://alignmentforum.org/posts/Abc123xyz/a-title"
            ),
            "https://www.lesswrong.com/posts/Abc123xyz",
        )

    def test_rejects_unrelated_or_malformed_links(self):
        self.assertIsNone(MODULE.canonical_post_url("https://example.com/posts/Abc123xyz"))
        self.assertIsNone(MODULE.canonical_post_url("https://www.lesswrong.com/posts/x"))


if __name__ == "__main__":
    unittest.main()
