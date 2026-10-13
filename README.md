# capuddddd 的个人博客

**写 Markdown，提交后自动发布。** 网站：[capuddddd.github.io](https://capuddddd.github.io)。

## 最方便的发布方法

1. 打开 [文章目录](https://github.com/capuddddd/capuddddd.github.io/tree/master/content/posts)，点击 **Add file → Create new file**。
2. 文件名写成 `2026-10-13-my-note.md`，复制下面的模板，修改标题、日期、分类和正文。
3. 点击 **Commit changes**，提交到 `master`。到 [Actions](https://github.com/capuddddd/capuddddd.github.io/actions/workflows/publish.yml) 查看 **Publish blog**，变成绿色后即发布完成。

```markdown
---
title: "我的第一篇笔记"
date: "2026-10-13"
category: "研究笔记"
slug: "my-note"
summary: "一句话介绍文章内容。"
draft: false
---

这里开始写正文。

## 小标题

普通文字、**加粗**、[链接](https://github.com/capuddddd)。
```

`title` 和 `date` 必填；`category` 默认“随笔”，不填 `summary` 时自动提取摘要。
`slug` 是链接的最后一段，推荐英文加短横线；不填时从文件名自动生成。
模板日期请改为文章实际日期。已有文章发布后，尽量保留 `date` 和 `slug`，避免改变链接。

完整写作示例在 [_template.md](content/posts/_template.md)。复制为新文件再编辑，保留模板本身。

## 修改、图片和草稿

- **修改文章**：打开对应 `.md` 文件，点击铅笔，编辑并提交。无需改 HTML 或运行脚本。
- **图片**：先把图片上传到仓库 `assets/` 目录，然后写 `![图片说明](/assets/my-image.png)`。页面会自动适应屏幕宽度。
- **草稿**：`draft: true` 不显示在博客；写完改成 `draft: false` 并提交即可发布。这个仓库是公开的，草稿源文件仍可被访问。
- **删除文章**：删除相应 `.md` 文件并提交；下次成功构建会清除对应页面并更新首页和归档。
- **格式错误**：构建失败会在 Actions 显示红色，线上保留上一次成功发布的版本；打开失败步骤查看文件名及错误提示，修正后再次提交。

支持标题、列表、链接、图片、代码块、引用和 Markdown 表格。年月归档会自动创建。
搜索在浏览器本地执行，不发送查询到外部服务。

## 本地预览（可选）

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8000 --directory _site
```

打开 `http://localhost:8000`。Windows 激活命令为 `.venv\Scripts\activate`。
测试命令：`python -m unittest discover -s tests -v`。

## 维护结构

- `content/posts/*.md`：文章唯一来源。
- `assets/`：作者上传的图片等静态资源。
- `scripts/`：Markdown 解析、模板构建和生成链接检查。
- `css/style.css`、`js/script.js`：简约样式及搜索/复制交互。
- `.github/workflows/publish.yml`：提交自动检查、构建和发布；PR 仅检查，不部署。
- `_site/`：构建产物，自动清理重建，已忽略，不需要提交。

GitHub Pages 的发布方式为 **GitHub Actions**。
官方发布参考：[GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。
Python Markdown 用法见 [官方扩展说明](https://python-markdown.github.io/extensions/)。

原文及文章 URL 已迁移保留；旧版 jQuery、fancyBox 与背景图片保留供历史对照，新版不加载它们。
第三方资源与许可状态见 [THIRD_PARTY.md](THIRD_PARTY.md)。
