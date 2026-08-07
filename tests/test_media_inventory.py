from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.media_inventory import build_youtube_inventory


class MediaInventoryTest(unittest.TestCase):
    def make_page(self, root: Path, name: str, url: str, title: str, video_id: str):
        page = root / "pages" / name
        page.mkdir(parents=True)
        (page / "manifest.json").write_text(
            json.dumps({"requested_url": url, "capture_started_at": 100}),
            encoding="utf-8",
        )
        (page / "page.html").write_text(
            f"""<html><head><title>{title}</title></head><body>
            <iframe title="Demo" src="https://www.youtube-nocookie.com/embed/{video_id}?x=1"></iframe>
            </body></html>""",
            encoding="utf-8",
        )

    def test_inventory_deduplicates_video_and_maps_articles(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "100"
            self.make_page(root, "one", "https://example.com/one", "One", "abcDEF_123")
            self.make_page(root, "two", "https://example.com/two", "Two", "abcDEF_123")
            data = build_youtube_inventory(
                [root],
                source="Example",
                media_root="media/youtube",
                generated_at_unix=123,
            )
            self.assertEqual(data["summary"]["videos"], 1)
            self.assertEqual(data["summary"]["articles"], 2)
            self.assertEqual(data["items"][0]["import_directory"], "media/youtube/abcDEF_123")
            self.assertEqual(
                [article["title"] for article in data["items"][0]["articles"]],
                ["One", "Two"],
            )

    def test_inventory_preserves_import_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "100"
            self.make_page(root, "one", "https://example.com/one", "One", "abcDEF_123")
            data = build_youtube_inventory(
                [root],
                source="Example",
                existing={
                    ("youtube", "abcDEF_123"): {
                        "status": "imported",
                        "imported_files": ["video.webm"],
                    }
                },
            )
            self.assertEqual(data["items"][0]["status"], "imported")
            self.assertEqual(data["items"][0]["imported_files"], ["video.webm"])


if __name__ == "__main__":
    unittest.main()
