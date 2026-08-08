from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.media_inventory import (
    build_substack_audio_inventory,
    build_substack_video_inventory,
    build_youtube_inventory,
)


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

    def test_substack_video_inventory_keeps_download_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "100"
            page = root / "pages" / "one"
            page.mkdir(parents=True)
            (page / "manifest.json").write_text(
                json.dumps(
                    {
                        "requested_url": "https://example.substack.com/p/one",
                        "capture_started_at": 100,
                    }
                ),
                encoding="utf-8",
            )
            (page / "page.html").write_text(
                '''<html><head><title>One</title></head><body>
<video data-video-id="media-123" data-video-title="Interview" poster="/poster.png">
<source src="/api/video/media-123?type=hls" type="application/x-mpegURL">
<source src="/api/video/media-123?type=mp4" type="video/mp4">
</video></body></html>''',
                encoding="utf-8",
            )
            data = build_substack_video_inventory(
                [root],
                source="Example",
                generated_at_unix=123,
            )
            self.assertEqual(data["summary"], {
                "videos": 1,
                "articles": 1,
                "statuses": {"pending_download": 1},
            })
            item = data["items"][0]
            self.assertEqual(item["media_id"], "media-123")
            self.assertEqual(item["articles"][0]["embed_title"], "Interview")
            self.assertEqual(
                item["articles"][0]["sources"][1]["url"],
                "https://example.substack.com/api/video/media-123?type=mp4",
            )

    def test_substack_audio_inventory_keeps_sources_captions_and_transcript_count(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "100"
            page = root / "pages" / "one"
            page.mkdir(parents=True)
            (page / "manifest.json").write_text(
                json.dumps(
                    {
                        "requested_url": "https://example.substack.com/p/one",
                        "capture_started_at": 100,
                    }
                ),
                encoding="utf-8",
            )
            (page / "page.html").write_text(
                '''<html><head><title>One</title></head><body>
<audio src="/api/v1/audio/upload/76180006-2724-40f6-870c-f8f8c5780bb1/src">
<track src="/captions.vtt" kind="captions" srclang="en" label="English">
</audio>
<div data-transcript-row-index="0">First</div>
<div data-transcript-row-index="1">Second</div></body></html>''',
                encoding="utf-8",
            )
            data = build_substack_audio_inventory(
                [root], source="Example", generated_at_unix=123
            )
            self.assertEqual(data["summary"]["audios"], 1)
            item = data["items"][0]
            self.assertEqual(
                item["media_id"], "76180006-2724-40f6-870c-f8f8c5780bb1"
            )
            article = item["articles"][0]
            self.assertEqual(article["embedded_transcript_rows"], 2)
            self.assertEqual(
                article["caption_tracks"][0]["url"],
                "https://example.substack.com/captions.vtt",
            )


if __name__ == "__main__":
    unittest.main()
