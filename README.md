# capuddddd.github.io

Hexo 生成的个人博客静态发布文件。仓库包含 HTML、CSS、JavaScript 和图片，
未包含 Hexo 的文章源码、`_config.yml` 或 `package.json`，因此不能从这里重建原始站点。

## 本地预览

```bash
python3 -m http.server 8000
```

在浏览器打开 `http://localhost:8000`，从仓库根目录提供服务，以兼容 `/css/` 等绝对路径。

## 维护

- 博客内容和主题应在原始 Hexo 项目编辑、生成后更新这里；直接修改生成文件可能被下次构建覆盖。
- 正式站点 URL 为 `https://capuddddd.github.io`，已替换 example.com 元数据、搜索和分享链接。
- 未提供 atom.xml 和 favicon.png，已移除相应无效入口；恢复文件后可恢复入口。
- 自有 `js/script.js` 用 DOM 属性和 text 写入分享及图片说明内容，避免把标题拼接成 HTML。
- 修改后的页面和脚本需检查搜索、分享、移动导航和图片浏览。

第三方资产及许可状态见 [THIRD_PARTY.md](THIRD_PARTY.md)。
没有恢复或伪造缺失的 Hexo 源工程。
