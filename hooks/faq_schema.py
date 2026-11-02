"""MkDocs hook: turn a page's "Frequently asked questions" section into FAQPage JSON-LD.

Answer engines read schema.org FAQPage markup. Instead of keeping a second copy of
every question in front matter, this hook parses the visible Markdown: every `### `
heading under a `## Frequently asked questions` heading is a question, and the
paragraphs below it (up to the next heading) are its answer. The result is stored in
`page.meta["faq_schema"]` and rendered by overrides/main.html.
"""

import json
import re

FAQ_HEADING = re.compile(r"^##\s+Frequently asked questions\s*$", re.IGNORECASE)
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MARKUP = re.compile(r"[*_`]|\{[^}]*\}|^!!!.*$|^\s*[-+] ", re.MULTILINE)


def _plain(text):
    text = LINK.sub(r"\1", text)
    text = MARKUP.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def on_page_markdown(markdown, page, config, files):
    items, question, answer, in_faq = [], None, [], False

    def flush():
        if question and answer:
            items.append((question, _plain("\n".join(answer))))

    for line in markdown.splitlines():
        if FAQ_HEADING.match(line):
            in_faq = True
            continue
        if not in_faq:
            continue
        if line.startswith("## "):
            break
        if line.startswith("### "):
            flush()
            question, answer = _plain(line[4:]), []
        elif question is not None:
            answer.append(line)
    flush()

    if items:
        page.meta["faq_schema"] = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in items
                ],
            },
            ensure_ascii=False,
        )
    return markdown
