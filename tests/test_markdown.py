import unittest

from util.epitome_lib.extraction import parse_timestamp
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
        self.assertAlmostEqual(word_coverage("one two two", "one two"), 2 / 3)


if __name__ == "__main__":
    unittest.main()
