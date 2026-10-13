"""Read author-maintained Markdown articles with validated YAML metadata."""
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import re

import markdown
from markdown.extensions.toc import slugify_unicode
import yaml


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def excerpt(body):
    parser = PlainText()
    parser.feed(body)
    text = " ".join(" ".join(parser.parts).split())
    return text[:120] + ("…" if len(text) > 120 else "")


def load_post(path):
    """A slug is one URL segment; date supplies the year/month/day segments."""
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)(.*)\Z", text, re.S)
    if not match:
        raise ValueError(f"{path.name}: article must start with YAML front matter (---).")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError(f"{path.name}: front matter must be a mapping.")
    for key in ("title", "date"):
        if key not in metadata:
            raise ValueError(f"{path.name}: missing {key}.")
    title = metadata["title"]
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{path.name}: title must be nonempty text.")
    try:
        published = date.fromisoformat(str(metadata["date"]))
    except ValueError as error:
        raise ValueError(f"{path.name}: date must be YYYY-MM-DD.") from error
    draft = metadata.get("draft", False)
    if not isinstance(draft, bool):
        raise ValueError(f"{path.name}: draft must be true or false, without quotes.")
    short_slug = metadata.get("slug", re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem))
    if not isinstance(short_slug, str) or not re.fullmatch(r"[\w-]+(?:\.[\w-]+)*", short_slug):
        raise ValueError(f"{path.name}: slug must be one segment of letters, numbers, dots or hyphens.")
    category = metadata.get("category", "随笔")
    summary = metadata.get("summary")
    if not isinstance(category, str) or not category.strip():
        raise ValueError(f"{path.name}: category must be text.")
    if summary is not None and not isinstance(summary, str):
        raise ValueError(f"{path.name}: summary must be text.")
    source = match.group(2).strip()
    if not source and not draft:
        raise ValueError(f"{path.name}: published article body is empty.")
    body = markdown.markdown(
        source, extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": slugify_unicode}}, output_format="html",
    )
    return {
        "title": title.strip(), "date": published.isoformat(),
        "slug": published.strftime("%Y/%m/%d/") + short_slug,
        "summary": summary if summary is not None else excerpt(body),
        "category": category.strip(), "body": body, "draft": draft,
    }


def load_posts(directory):
    posts = []
    seen = set()
    for path in sorted(Path(directory).glob("*.md")):
        post = load_post(path)
        if post["draft"]:
            continue
        if post["slug"] in seen:
            raise ValueError(f"{path.name}: duplicate article URL {post['slug']}.")
        seen.add(post["slug"])
        posts.append(post)
    return sorted(posts, key=lambda post: (post["date"], post["slug"]), reverse=True)
