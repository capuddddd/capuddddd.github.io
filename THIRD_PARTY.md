# 第三方资源

保留已有第三方文件的许可标头，不把它们作为自有代码重新格式化。

| 资源 | 位置 | 已见说明 |
| --- | --- | --- |
| jQuery 3.6.4 | js/jquery-3.6.4.min.js | OpenJS 作者信息及 jquery.org/license 链接 |
| fancyBox 3.5.7 | fancybox/ | 文件标头写明 GPLv3 开源用途或商业许可 |
| Fork Awesome 1.2.0 | HTML 中 CDN CSS | 外部资源，需记录适用许可 |
| Hexo / 主题 | 生成 HTML、CSS、script.js | 未提供主题来源及完整许可文件 |
| banner.jpg | css/images/ | 未提供来源与授权说明 |

这是已有资源清单；尚未完成完整许可证审核。发布前需要补齐上游版权/许可文本、
主题来源、图片授权以及自有代码的许可证，不应给整仓库随意套用一个许可证。

2026-10-13 博客改版：新版页面使用原生 JavaScript 和自有 CSS，不再加载上述第三方脚本、图标 CDN 或旧背景图片。旧文件保留供历史对照；Hello World 正文仍保留原 Hexo 介绍及相关链接。

构建环境依赖 Python-Markdown 3.8.2 与 PyYAML 6.0.2，版本固定在 requirements.txt；它们用于构建，不作为浏览器脚本加载。来源：[Python-Markdown](https://github.com/Python-Markdown/markdown)、[PyYAML](https://github.com/yaml/pyyaml)。
