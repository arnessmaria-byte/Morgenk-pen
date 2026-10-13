// Setter sammen spillet til én fil.
//   voffgenics.html: sideinnholdet slik Artifact-publisering vil ha det (uten doctype/head/body)
//   index.html:      frittstående side som kan åpnes rett i nettleseren
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'src');
const head = readFileSync(join(src, 'head.html'), 'utf8');
const js = readdirSync(src).filter(f => f.endsWith('.js')).sort()
  .map(f => `// ===== ${f} =====\n` + readFileSync(join(src, f), 'utf8')).join('\n');

const body = `${head}
<div id="app"></div>
<div id="modal-root"></div>
<div id="toast" class="toast" role="status" aria-live="polite" hidden></div>
<script>
(() => {
'use strict';
${js}
})();
</script>
`;
writeFileSync(join(here, 'voffgenics.html'), body);
writeFileSync(join(here, 'index.html'), `<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
</head>
<body>
${body}</body>
</html>
`);
console.log(`Bygget voffgenics.html (${(body.length / 1024).toFixed(1)} KB) og index.html`);
