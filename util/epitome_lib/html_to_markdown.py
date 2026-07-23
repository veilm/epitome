"""Dependency-free HTML-to-Markdown conversion for extracted article HTML."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
import re
from typing import Iterable
from urllib.parse import urljoin


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "div",
    "dl",
    "figure",
    "figcaption",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "iframe",
    "main",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "ul",
    "video",
    "audio",
}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["Node | str"] = field(default_factory=list)


class TreeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag.lower(), {name: value or "" for name, value in attrs})
        self.stack[-1].children.append(node)
        if node.tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def text_content(node: Node | str) -> str:
    if isinstance(node, str):
        return node
    return "".join(text_content(child) for child in node.children)


def normalize_inline(value: str) -> str:
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    return value.strip()


def strip_window_helper(value: str) -> str:
    return re.sub(r"\s*\(?opens in a new window\)?\s*", "", value, flags=re.I)


def best_image_source(node: Node) -> str:
    source = node.attrs.get("src") or node.attrs.get("data-src") or ""
    srcset = node.attrs.get("srcset", "")
    if srcset:
        candidates = [part.strip().split()[0] for part in srcset.split(",") if part.strip()]
        if candidates:
            source = candidates[-1]
    return source


class MarkdownRenderer:
    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url

    def inline(self, item: Node | str) -> str:
        if isinstance(item, str):
            return re.sub(r"\s+", " ", item)
        tag = item.tag
        content = "".join(self.inline(child) for child in item.children)
        clean = normalize_inline(content)
        leading = " " if content[:1].isspace() else ""
        trailing = " " if content[-1:].isspace() else ""
        if tag == "a":
            label = strip_window_helper(clean)
            href = urljoin(self.base_url, item.attrs.get("href", ""))
            if not href:
                return leading + label + trailing
            return leading + f"[{label or href}]({href})" + trailing
        if tag in {"strong", "b"} and clean:
            return leading + f"**{clean}**" + trailing
        if tag in {"em", "i"} and clean:
            return leading + f"*{clean}*" + trailing
        if tag == "code" and clean:
            ticks = "``" if "`" in clean else "`"
            return leading + f"{ticks}{clean}{ticks}" + trailing
        if tag == "br":
            return "  \n"
        if tag == "img":
            source = urljoin(self.base_url, best_image_source(item))
            alt = normalize_inline(item.attrs.get("alt", ""))
            return f"![{alt}]({source})" if source else alt
        if tag == "sup" and clean:
            return f"^{clean}"
        return content

    def inline_sequence(self, items: Iterable[Node | str]) -> str:
        pieces = []
        previous = None
        for child in items:
            if (
                isinstance(previous, Node)
                and previous.tag == "a"
                and isinstance(child, Node)
                and child.tag == "a"
            ):
                pieces.append(" ")
            pieces.append(self.inline(child))
            previous = child
        return normalize_inline("".join(pieces))

    def inline_children(self, node: Node) -> str:
        return self.inline_sequence(node.children)

    def table(self, node: Node) -> str:
        rows: list[tuple[list[str], bool]] = []
        for row in descendants(node, "tr"):
            cells = [
                cell
                for cell in row.children
                if isinstance(cell, Node) and cell.tag in {"th", "td"}
            ]
            if not cells:
                continue
            rows.append(
                ([self.inline_children(cell).replace("|", "\\|") for cell in cells], any(cell.tag == "th" for cell in cells))
            )
        if not rows:
            return ""
        width = max(len(cells) for cells, _ in rows)
        padded = [cells + [""] * (width - len(cells)) for cells, _ in rows]
        header = padded[0]
        body = padded[1:]
        lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
        lines.extend("| " + " | ".join(row) + " |" for row in body)
        return "\n".join(lines)

    def media(self, node: Node) -> str:
        sources = []
        direct = node.attrs.get("src")
        if direct:
            sources.append(direct)
        sources.extend(
            child.attrs.get("src", "")
            for child in descendants(node, "source")
            if child.attrs.get("src")
        )
        label = node.tag.capitalize()
        title = normalize_inline(node.attrs.get("title", ""))
        if not sources:
            if node.tag == "iframe" and title:
                return f"_Embedded media: {title}_"
            return ""
        return "\n\n".join(
            f"[{title or label}]({urljoin(self.base_url, source)})" for source in dict.fromkeys(sources)
        )

    def list_block(self, node: Node, ordered: bool) -> str:
        lines = []
        number = 1
        for child in node.children:
            if not isinstance(child, Node) or child.tag != "li":
                continue
            inline_parts = []
            nested = []
            for part in child.children:
                if isinstance(part, Node) and part.tag in {"ul", "ol"}:
                    nested.append(self.list_block(part, part.tag == "ol"))
                elif isinstance(part, Node) and part.tag in BLOCK_TAGS:
                    inline_parts.append(self.render_block(part))
                else:
                    inline_parts.append(self.inline(part))
            content = normalize_inline(" ".join(inline_parts))
            if ordered:
                content = re.sub(rf"^{number}\s+", "", content)
            prefix = f"{number}." if ordered else "-"
            lines.append(f"{prefix} {content}".rstrip())
            for sublist in nested:
                lines.extend("  " + line for line in sublist.splitlines())
            number += 1
        return "\n".join(lines)

    def container(self, node: Node) -> str:
        blocks = []
        inline_buffer: list[Node | str] = []

        def flush() -> None:
            if not inline_buffer:
                return
            value = self.inline_sequence(inline_buffer)
            if value:
                blocks.append(value)
            inline_buffer.clear()

        for child in node.children:
            if isinstance(child, Node) and child.tag in BLOCK_TAGS:
                flush()
                value = self.render_block(child).strip()
                if value:
                    blocks.append(value)
            else:
                inline_buffer.append(child)
        flush()
        deduplicated = []
        for block in blocks:
            if not deduplicated or block != deduplicated[-1]:
                deduplicated.append(block)
        return "\n\n".join(deduplicated)

    def render_block(self, node: Node) -> str:
        tag = node.tag
        if re.fullmatch(r"h[1-6]", tag):
            value = self.inline_children(node)
            return f"{'#' * int(tag[1])} {value}" if value else ""
        if tag == "p":
            return self.inline_children(node)
        if tag == "pre":
            raw = text_content(node).strip("\n")
            code = next((child for child in node.children if isinstance(child, Node) and child.tag == "code"), None)
            language = ""
            if code:
                match = re.search(r"(?:language-|lang-)([\w+-]+)", code.attrs.get("class", ""))
                language = match.group(1) if match else ""
            return f"```{language}\n{raw}\n```"
        if tag == "blockquote":
            value = self.container(node)
            return "\n".join("> " + line if line else ">" for line in value.splitlines())
        if tag in {"ul", "ol"}:
            return self.list_block(node, tag == "ol")
        if tag == "table":
            return self.table(node)
        if tag == "hr":
            return "---"
        if tag in {"video", "audio", "iframe"}:
            return self.media(node)
        if tag == "img":
            return self.inline(node)
        return self.container(node)

    def render(self, html: str) -> str:
        parser = TreeParser()
        parser.feed(html)
        parser.close()
        value = self.container(parser.root)
        value = re.sub(r"[ \t]+\n", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip() + "\n"


def descendants(node: Node, tag: str) -> Iterable[Node]:
    for child in node.children:
        if not isinstance(child, Node):
            continue
        if child.tag == tag:
            yield child
        yield from descendants(child, tag)


def word_coverage(source: str, markdown: str) -> float:
    words = re.compile(r"[\w’'-]+", re.UNICODE)
    source_words = Counter(word.lower() for word in words.findall(source))
    markdown_words = Counter(word.lower() for word in words.findall(markdown))
    total = sum(source_words.values())
    if not total:
        return 1.0
    matched = sum(min(count, markdown_words[word]) for word, count in source_words.items())
    return matched / total
