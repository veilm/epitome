(() => {
  const supplied = __EPITOME_OPTIONS__;
  const options = Object.assign(
    {
      rootSelectors: [],
      excludeSelectors: [],
      excludeTextExact: [],
      cutAtHeadings: [],
    },
    supplied,
  );

  function normalized(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function largest(selector) {
    const candidates = Array.from(document.querySelectorAll(selector));
    candidates.sort(
      (a, b) => normalized(b.textContent).length - normalized(a.textContent).length,
    );
    return candidates[0] || null;
  }

  const selectors = options.rootSelectors.concat(["article", "main", "[role=main]"]);
  let sourceRoot = null;
  let rootSelector = "body";
  for (const selector of selectors) {
    const candidate = largest(selector);
    if (candidate && normalized(candidate.textContent).length >= 100) {
      sourceRoot = candidate;
      rootSelector = selector;
      break;
    }
  }
  if (!sourceRoot) sourceRoot = document.body;

  const authors = [];
  for (const section of sourceRoot.querySelectorAll('[data-testid="author-list"]')) {
    const heading = section.querySelector("h1,h2,h3,h4,h5,h6");
    if (normalized(heading?.textContent).toLowerCase() !== "author") continue;
    const copy = section.cloneNode(true);
    copy.querySelector("h1,h2,h3,h4,h5,h6")?.remove();
    const value = normalized(copy.textContent);
    if (value) authors.push(value);
  }
  sourceRoot.querySelectorAll('[rel="author"]').forEach((element) => {
    const value = normalized(element.textContent);
    if (value) authors.push(value);
  });

  const structuredArticles = [];
  function collectStructured(value) {
    if (Array.isArray(value)) {
      value.forEach(collectStructured);
      return;
    }
    if (!value || typeof value !== "object") return;
    const type = value["@type"];
    const types = Array.isArray(type) ? type : [type];
    if (
      value.datePublished ||
      value.author ||
      types.some((name) => /^(Article|BlogPosting|NewsArticle)$/i.test(name || ""))
    ) {
      structuredArticles.push(value);
    }
    if (value["@graph"]) collectStructured(value["@graph"]);
  }
  document.querySelectorAll('script[type="application/ld+json"]').forEach((script) => {
    try {
      collectStructured(JSON.parse(script.textContent || "null"));
    } catch (_) {
      // Invalid optional metadata should not prevent content extraction.
    }
  });
  structuredArticles.forEach((article) => {
    const values = Array.isArray(article.author) ? article.author : [article.author];
    values.forEach((author) => {
      const value = normalized(typeof author === "string" ? author : author?.name);
      if (value) authors.push(value);
    });
  });

  const root = sourceRoot.cloneNode(true);
  const genericExcludes = [
    "script",
    "style",
    "noscript",
    "template",
    "nav",
    "form",
    "button",
    "dialog",
    '[role="status"]',
    ".web-nav-hidden",
  ];
  for (const selector of genericExcludes.concat(options.excludeSelectors)) {
    try {
      root.querySelectorAll(selector).forEach((element) => element.remove());
    } catch (_) {
      // A bad optional site selector should not destroy generic extraction.
    }
  }

  const excludedText = new Set(options.excludeTextExact.map((value) => normalized(value)));
  if (excludedText.size) {
    Array.from(root.querySelectorAll("*")).reverse().forEach((element) => {
      if (excludedText.has(normalized(element.textContent))) element.remove();
    });
  }

  const cutoffNames = new Set(options.cutAtHeadings.map((value) => normalized(value).toLowerCase()));
  if (cutoffNames.size) {
    const headings = Array.from(root.querySelectorAll("h1,h2,h3,h4,h5,h6"));
    const cutoffHeading = headings.find((heading) =>
      cutoffNames.has(normalized(heading.textContent).toLowerCase()),
    );
    if (cutoffHeading) {
      let cutoff = cutoffHeading;
      while (cutoff.parentElement && cutoff.parentElement !== root) {
        cutoff = cutoff.parentElement;
      }
      let current = cutoff;
      while (current) {
        const next = current.nextSibling;
        current.remove();
        current = next;
      }
    }
  }

  root.querySelectorAll("a[href]").forEach((element) => {
    element.setAttribute("href", new URL(element.getAttribute("href"), location.href).href);
  });
  root.querySelectorAll("img").forEach((element) => {
    for (const attribute of ["src", "data-src"]) {
      const value = element.getAttribute(attribute);
      if (value) element.setAttribute(attribute, new URL(value, location.href).href);
    }
  });
  root.querySelectorAll("video,audio,source,iframe").forEach((element) => {
    const value = element.getAttribute("src");
    if (value) element.setAttribute("src", new URL(value, location.href).href);
  });

  const canonical =
    document.querySelector('link[rel="canonical"]')?.href || location.href;
  const headline =
    sourceRoot.querySelector('[data-article-hero-copy-region="headline"]') ||
    sourceRoot.querySelector("h1");
  const subhead = sourceRoot.querySelector('[data-article-hero-copy-region="subhead"]');
  let description =
    normalized(subhead?.textContent) ||
    document.querySelector('meta[name="description"]')?.content ||
    document.querySelector('meta[property="og:description"]')?.content ||
    "";
  if (!normalized(description)) {
    description = Array.from(sourceRoot.querySelectorAll("p"))
      .map((element) => normalized(element.textContent))
      .find((value) => value.length >= 80) || "";
  }
  const heroMeta = sourceRoot.querySelector('[data-article-hero-copy-region="meta"]');
  const heroTime = heroMeta?.querySelector("time");
  const publishedMeta =
    document.querySelector('meta[property="article:published_time"]')?.content ||
    document.querySelector('meta[name="date"]')?.content ||
    structuredArticles.find((article) => article.datePublished)?.datePublished ||
    "";
  const visibleDate = Array.from(sourceRoot.querySelectorAll("*")).find((element) => {
    if (element.children.length) return false;
    return /^(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+\d{4}$/i.test(
      normalized(element.textContent),
    );
  });
  const publishedDisplay =
    normalized(heroTime?.textContent) ||
    normalized(heroMeta?.querySelector("p")?.textContent) ||
    normalized(heroMeta?.textContent) ||
    normalized(visibleDate?.textContent) ||
    normalized(publishedMeta);

  return {
    url: location.href,
    canonical,
    title: normalized(headline?.textContent) || document.title,
    documentTitle: document.title,
    description: normalized(description),
    language: document.documentElement.lang || "",
    published: publishedMeta || heroTime?.getAttribute("datetime") || publishedDisplay,
    publishedDisplay,
    authors: Array.from(new Set(authors)),
    rootSelector,
    documentHtml: document.documentElement.outerHTML,
    contentHtml: root.innerHTML,
    sourceText: normalized(root.textContent),
    documentHtmlCharacters: document.documentElement.outerHTML.length,
    mediaCount: root.querySelectorAll("img,video,audio,iframe").length,
    mediaWithoutSource: Array.from(root.querySelectorAll("img,video,audio,iframe")).filter(
      (element) =>
        !element.getAttribute("src") &&
        !element.getAttribute("srcset") &&
        !element.querySelector("source[src]"),
    ).length,
  };
})()
