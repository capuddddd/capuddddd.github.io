# capuddddd 的个人博客

GitHub Pages 上的静态博客：暖白背景、单栏阅读、时间归档和浏览器内文章搜索。
文章保留原有 URL，页面不依赖第三方 CDN、框架或外部字体。

## 修改文章和页面

- `content/posts.json`：文章标题、日期、摘要、分类、URL 路径和 HTML 正文。
- `scripts/build_site.py`：页面模板与生成逻辑。
- `css/style.css`：桌面与手机布局。
- `js/script.js`：搜索标题/摘要/分类，复制文章链接。

正文 HTML 是可信作者内容，仅在这里编辑自己的文章；模板会转义标题与摘要。
修改内容或模板后，从仓库根目录运行：

```bash
python3 scripts/build_site.py
python3 -m http.server 8000
```

打开 `http://localhost:8000` 检查页面，将源文件与生成的 HTML 一起提交到 `master`。
GitHub Pages 继续从原有仓库发布。直接改生成 HTML 会被下次构建覆盖。

首页展示文章摘要，文章页保留完整正文。搜索在本地执行，不发送查询给外部搜索引擎。
复制链接在浏览器禁止剪贴板访问时提供地址栏复制提示。
移动布局、键盘焦点、跳到正文和减少动态效果偏好均有对应支持。

原 Hexo 生成内容已提取为可维护的文章数据；旧版 jQuery、fancyBox 和 banner 文件
保留在仓库，但新版页面不加载它们。第三方许可清单见 [THIRD_PARTY.md](THIRD_PARTY.md)。
本次更新保留历史正文，没有代作者重新选择文章内容的许可证。
