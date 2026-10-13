import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_site
from check_site import check
from post_loader import load_posts, load_post


class PublicationTest(unittest.TestCase):
    def article(self, root, name="2027-01-02-new-note.md", extra="", body="## 标题\n\n**加粗**正文。"):
        folder = root / "content/posts"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / name
        path.write_text(f'---\ntitle: "文章标题"\ndate: "2027-01-02"\n{extra}---\n\n{body}\n')
        return path

    def fixtures(self, root):
        for asset in ("css/style.css", "js/script.js"):
            path = root / asset
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("/* fixture */")
        (root / "assets").mkdir()
        (root / "assets/image.png").write_bytes(b"fixture")

    def test_markdown_metadata_and_derived_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            post = load_post(self.article(root))
            self.assertEqual(post["slug"], "2027/01/02/new-note")
            self.assertIn("<strong>加粗</strong>", post["body"])
            self.assertEqual(post["category"], "随笔")
            self.assertIn("正文", post["summary"])

    def test_drafts_are_not_published(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.article(root, extra="draft: true\n")
            self.assertEqual(load_posts(root / "content/posts"), [])

    def test_invalid_date_and_slug_and_duplicate_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self.article(root, extra='slug: "../../index"\n')
            with self.assertRaises(ValueError):
                load_post(path)
            path.write_text(path.read_text().replace('../../index', 'valid').replace('2027-01-02', '2027-02-30'))
            with self.assertRaises(ValueError):
                load_post(path)
            self.article(root, extra='slug: "same"\n')
            self.article(root, name="second.md", extra='slug: "same"\n')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                load_posts(root / "content/posts")

    def test_build_dynamic_archives_assets_and_remove_deleted_article(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixtures(root)
            article = self.article(root, body='![图](/assets/image.png)\n\n## 标题\n\n[锚点](#标题)')
            self.article(root, name="draft.md", extra='draft: true\n', body="Unpublished draft")
            output = root / "_site"
            with patch.object(build_site, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
                build_site.build(output)
                check(output)
                self.assertTrue((output / "archives/2027/01/index.html").is_file())
                page = output / "2027/01/02/new-note/index.html"
                self.assertTrue(page.is_file())
                self.assertFalse((output / "content").exists())
                self.assertFalse((output / "2027/01/02/draft").exists())
                self.assertIn("文章标题", (output / "index.html").read_text())
                article.unlink()
                build_site.build(output)
                check(output)
                self.assertFalse(page.exists())
                self.assertFalse((output / "archives/2027").exists())

    def test_cannot_clear_source_or_unknown_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixtures(root)
            self.article(root)
            with patch.object(build_site, "ROOT", root):
                with self.assertRaises(ValueError):
                    build_site.build(root / "content")
                output = root / "_site"
                output.mkdir()
                keep = output / "keep.txt"
                keep.write_text("keep")
                with self.assertRaises(ValueError):
                    build_site.build(output)
                self.assertEqual(keep.read_text(), "keep")

    def test_link_validation_catches_missing_image(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixtures(root)
            self.article(root, body='![图](/assets/missing.png)')
            with patch.object(build_site, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
                output = root / "_site"
                build_site.build(output)
                with self.assertRaisesRegex(ValueError, 'missing.png'):
                    check(output)


if __name__ == "__main__":
    unittest.main()
