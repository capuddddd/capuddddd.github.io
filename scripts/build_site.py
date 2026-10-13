"""Build the personal blog from tracked article content using Python only."""
import argparse
from collections import defaultdict
import shutil
from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://capuddddd.github.io'
from post_loader import load_posts

OUTPUT = ROOT / "_site"


def url(post):
    return '/' + quote(post['slug'], safe='/') + '/'


def layout(title, description, path, main, active='home', article=False):
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · capuddddd</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="{'article' if article else 'website'}">
  <meta property="og:locale" content="zh_CN">
  <meta property="og:site_name" content="capuddddd">
  <meta property="og:url" content="{BASE}{path}">
  <meta name="theme-color" content="#f8f7f3">
  <link rel="canonical" href="{BASE}{path}">
  <link rel="stylesheet" href="/css/style.css">
  <script src="/js/script.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header shell">
    <a class="brand" href="/" aria-label="capuddddd 首页"><span class="brand-mark" aria-hidden="true">c.</span>capuddddd</a>
    <nav aria-label="主导航">
      <a href="/" {'aria-current="page"' if active == 'home' else ''}>首页</a>
      <a href="/archives/" {'aria-current="page"' if active == 'archives' else ''}>归档</a>
      <a href="https://github.com/capuddddd" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a>
    </nav>
  </header>
  <main id="main" class="shell">{main}</main>
  <footer class="site-footer shell"><span>© 2026 capuddddd</span><span>记录，思考，继续探索。</span><a href="#" class="back-top">回到顶部 ↑</a></footer>
</body>
</html>
'''


def rows(posts):
    return '\n'.join(f'''<article class="post-row" data-search="{escape(p['title']+' '+p['summary']+' '+p['category'], quote=True)}">
      <div class="post-meta"><time datetime="{p['date']}">{p['date'].replace('-', '.')}</time><span>{escape(p['category'])}</span></div>
      <div class="post-copy"><h3><a href="{url(p)}">{escape(p['title'])}</a></h3><p>{escape(p['summary'])}</p></div>
      <a class="post-arrow" href="{url(p)}" aria-label="阅读 {escape(p['title'], quote=True)}">↗</a>
    </article>''' for p in posts)


def write(path, text):
    destination = OUTPUT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text)




def build(output):
    global OUTPUT
    candidate = Path(output)
    if candidate.is_symlink():
        raise ValueError("Output must not be a symbolic link.")
    OUTPUT = candidate.resolve()
    # The output is a dedicated artifact directory; refuse source-tree overlap.
    if OUTPUT == ROOT or ROOT.is_relative_to(OUTPUT):
        raise ValueError("Output must not be the repository or one of its ancestors.")
    for source in (ROOT / "content", ROOT / "scripts", ROOT / "css", ROOT / "js", ROOT / "assets", ROOT / ".git"):
        if OUTPUT == source or OUTPUT.is_relative_to(source) or source.is_relative_to(OUTPUT):
            raise ValueError("Output must not overlap source or Git directories.")
    POSTS = load_posts(ROOT / "content/posts")
    if OUTPUT.exists():
        if not OUTPUT.is_dir() or (any(OUTPUT.iterdir()) and not (OUTPUT / ".blog-build").is_file()):
            raise ValueError("Refusing to clear a directory not created by the blog builder.")
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    for asset in ("css/style.css", "js/script.js"):
        destination = OUTPUT / asset
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / asset, destination)
    if (ROOT / "assets").exists():
        shutil.copytree(ROOT / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    (OUTPUT / ".nojekyll").touch()
    (OUTPUT / ".blog-build").touch()

    hero = '''<section class="intro" aria-labelledby="intro-title">
      <p class="eyebrow"><span class="status-dot" aria-hidden="true"></span> 个人博客 / PERSONAL NOTES</p>
      <h1 id="intro-title">把想法写下来<span class="accent">。</span></h1>
      <p class="intro-description">研究笔记、代码实践，以及值得留下的日常。</p>
      <a class="text-link" href="#posts">从最近的记录开始 <span aria-hidden="true">↓</span></a>
      <span class="intro-number" aria-hidden="true">01 — NOTES</span>
    </section>'''
    listing = f'''<section id="posts" class="post-section" aria-labelledby="posts-title">
      <div class="section-heading"><div><p class="eyebrow">THE JOURNAL</p><h2 id="posts-title">最近记录 <span class="count">{len(POSTS):02}</span></h2></div>
      <label class="search-label"><span class="sr-only">搜索文章</span><input id="post-search" type="search" placeholder="搜索记录…" autocomplete="off" aria-controls="post-list"></label></div>
      <div id="post-list">{rows(POSTS)}</div>
      <p id="search-status" class="search-status" role="status" hidden></p>
      <a class="text-link archive-link" href="/archives/">查看全部归档 <span aria-hidden="true">→</span></a>
    </section>'''
    write('index.html', layout('个人记录', '研究笔记、代码实践，以及值得留下的日常。', '/', hero+listing))
    groups = defaultdict(list)
    for post in POSTS:
        groups[post["date"][:4]].append(post)
        groups[post["date"][:7].replace("-", "/")].append(post)
    archives = {"": POSTS, **groups}
    for key, selected in sorted(archives.items()):
        path = "archives" + ("/" + key if key else "")
        heading = "文章归档" if not key else key.replace("/", " 年 ") + (" 月的记录" if "/" in key else " 年的记录")
        sections = []
        for year in sorted({p["date"][:4] for p in selected}, reverse=True):
            yearly = [p for p in selected if p["date"].startswith(year)]
            months = sorted({p["date"][5:7] for p in yearly}, reverse=True)
            month_links = " ".join(f'<a class="text-link" href="/archives/{year}/{month}/">{month} 月</a>' for month in months)
            sections.append(f'<section class="post-section" aria-labelledby="year-{year}"><div class="section-heading"><h2 id="year-{year}">{year} <span class="count">{len(yearly):02}</span></h2><div>{month_links}</div></div>{rows(yearly)}</section>')
        main = f'<section class="archive-intro"><p class="eyebrow">THE ARCHIVE</p><h1>{heading}<span class="accent">。</span></h1><p>共 {len(selected)} 篇记录，按时间排列。</p></section>' + "".join(sections)
        write(path + '/index.html', layout(heading, '按时间浏览 capuddddd 的文章和笔记。', '/' + path + '/', main, 'archives'))
    for post in POSTS:
        other=[p for p in POSTS if p is not post]
        adjacent=''.join(f'<a class="related-post" href="{url(p)}"><span>继续阅读</span><strong>{escape(p["title"])}</strong><span aria-hidden="true">→</span></a>' for p in other)
        main=f'''<div class="reading-layout"><a class="text-link back-link" href="/">← 返回全部记录</a>
        <article class="reading-article"><header class="reading-header"><p class="eyebrow">{escape(post['category'])}</p><h1>{escape(post['title'])}</h1><div class="post-meta"><time datetime="{post['date']}">{post['date'].replace('-', '.')}</time><span>capuddddd</span></div></header>
        <div class="article-entry">{post['body']}</div>
        <footer class="reading-footer"><span>记录于 {post['date'].replace('-', '.')}</span><button class="copy-link" type="button">复制文章链接 ↗</button><span id="copy-status" class="sr-only" role="status"></span></footer></article>
        <nav class="related-nav" aria-label="其他文章">{adjacent}</nav></div>'''
        write(post['slug']+'/index.html',layout(post['title'],post['summary'],url(post),main,article=True))
    print(f'Built {len(list(OUTPUT.rglob("*.html")))} pages from {len(POSTS)} published Markdown articles.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the Markdown blog into _site.")
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    build(args.output)
