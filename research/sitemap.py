"""Pure sitemap parsing helpers used by research/list_sitemap_urls."""

from xml.etree import ElementTree


def rendered_xml(text: str) -> bytes:
    """Recover XML from Chromium's XML viewer or a plain-text response."""
    starts = [
        position
        for marker in ("<?xml", "<urlset", "<sitemapindex")
        if (position := text.find(marker)) >= 0
    ]
    if not starts:
        raise ValueError("rendered page contains no sitemap XML")
    return text[min(starts) :].strip().encode()


def locations(xml: bytes) -> tuple[list[str], list[str]]:
    root = ElementTree.fromstring(xml)
    tag = root.tag.rsplit("}", 1)[-1]
    locs = [
        element.text.strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text
    ]
    if tag == "sitemapindex":
        return locs, []
    if tag == "urlset":
        return [], locs
    raise ValueError(f"unsupported sitemap root: {tag}")
