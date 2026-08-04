import unittest

from util.epitome_lib.extraction import (
    convert_extraction,
    missing_note_targets,
    parse_timestamp,
    site_options,
)
from util.epitome_lib.html_to_markdown import MarkdownRenderer, word_coverage


class MarkdownTest(unittest.TestCase):
    def test_common_article_blocks(self):
        html = """
        <h1>Example</h1>
        <p>A <strong>bold</strong> paragraph with <a href="/more">a link</a>.</p>
        <ul><li>First</li><li>Second</li></ul>
        <blockquote><p>Quoted text</p></blockquote>
        <table><thead><tr><th>Name</th><th>Value</th></tr></thead>
        <tbody><tr><td>A</td><td>1</td></tr></tbody></table>
        <pre><code class="language-python">print("hello")</code></pre>
        <img src="/image.png" alt="Diagram">
        """
        markdown = MarkdownRenderer("https://example.com/article").render(html)
        self.assertIn("# Example", markdown)
        self.assertIn("A **bold** paragraph", markdown)
        self.assertIn("[a link](https://example.com/more)", markdown)
        self.assertIn("- First\n- Second", markdown)
        self.assertIn("> Quoted text", markdown)
        self.assertIn("| Name | Value |", markdown)
        self.assertIn('```python\nprint("hello")\n```', markdown)
        self.assertIn("![Diagram](https://example.com/image.png)", markdown)
        self.assertIn("paragraph with [a link]", markdown)

    def test_inline_formatting_preserves_boundary_spaces(self):
        markdown = MarkdownRenderer().render(
            "<p><b><i>Label:</i></b><i> explanation</i></p>"
        )
        self.assertEqual(markdown, "***Label:*** *explanation*\n")

    def test_adjacent_links_are_separated(self):
        markdown = MarkdownRenderer().render(
            '<p><a href="/one">One</a><a href="/two">Two</a></p>'
        )
        self.assertEqual(markdown, "[One](/one) [Two](/two)\n")

    def test_timestamp_and_coverage(self):
        self.assertEqual(parse_timestamp("1970-01-01T00:00:10Z"), 10)
        self.assertEqual(parse_timestamp("January 1, 1970"), 0)
        self.assertEqual(parse_timestamp("Jul 22, 2026"), 1784678400)
        self.assertAlmostEqual(word_coverage("one two two", "one two"), 2 / 3)

    def test_anthropic_and_claude_site_rules(self):
        anthropic = site_options("https://www.anthropic.com/news/example")
        self.assertEqual(anthropic["rootSelectors"], ["article"])
        self.assertEqual(anthropic["cutAtHeadings"], ["Related content"])

        claude = site_options("https://claude.com/blog/example")
        self.assertEqual(claude["rootSelectors"], ["main"])
        self.assertEqual(claude["cutAtHeadings"], ["Related posts"])

    def test_missing_note_targets_are_reported(self):
        html = """
        <p>Claims<a href="#citation-bottom-1">1</a>
        and<a href="https://example.com/a#citation-bottom-2">2</a>.</p>
        <ol><li id="citation-bottom-1">First note.</li></ol>
        """
        self.assertEqual(missing_note_targets(html), ["citation-bottom-2"])
        _, report = convert_extraction(
            {
                "canonical": "https://example.com/a",
                "contentHtml": html,
                "sourceText": "Claims 1 and 2. First note.",
                "title": "Article",
            },
            100,
        )
        self.assertIn("citation-bottom-2", report["warnings"][-1])


if __name__ == "__main__":
    unittest.main()
