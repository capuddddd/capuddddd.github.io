/* Native browser interactions; no framework or CDN required. */
'use strict';

const search = document.querySelector('#post-search');
if (search) {
  const rows = Array.from(document.querySelectorAll('.post-row'));
  const status = document.querySelector('#search-status');
  search.addEventListener('input', () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const row of rows) {
      row.hidden = !row.dataset.search.toLocaleLowerCase().includes(query);
      if (!row.hidden) visible += 1;
    }
    status.hidden = !query;
    status.textContent = visible ? `找到 ${visible} 篇记录` : '暂无匹配的记录，试试其他关键词。';
  });
}

const copyButton = document.querySelector('.copy-link');
if (copyButton) {
  copyButton.addEventListener('click', async () => {
    const status = document.querySelector('#copy-status');
    const canonical = document.querySelector('link[rel="canonical"]').href;
    try {
      await navigator.clipboard.writeText(canonical);
      copyButton.textContent = '链接已复制 ✓';
      status.textContent = '文章链接已复制';
    } catch {
      status.textContent = '无法自动复制，请复制地址栏中的文章链接。';
      copyButton.textContent = '请复制地址栏链接';
    }
  });
}
