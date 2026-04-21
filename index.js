const { chromium } = require('playwright');
const fs = require('fs');

const BASE_URL = 'https://magnetic-make-older-coordination.trycloudflare.com';

const viewports = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
];

(async () => {
  const browser = await chromium.launch();

  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('🔍 Escaneando links...');
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });

  // Obtener links internos
  let links = await page.$$eval('a', as =>
    as.map(a => a.href)
  );

  links = [...new Set(links)].filter(link =>
    link.startsWith(BASE_URL)
  );

  // incluir home
  if (!links.includes(BASE_URL)) links.push(BASE_URL);

  console.log(`✅ Encontradas ${links.length} páginas`);

  // crear carpeta
  if (!fs.existsSync('screenshots')) {
    fs.mkdirSync('screenshots');
  }

  for (const link of links) {
    for (const vp of viewports) {
      const ctx = await browser.newContext({
        viewport: { width: vp.width, height: vp.height }
      });

      const p = await ctx.newPage();

      console.log(`📸 ${link} (${vp.name})`);

      try {
        await p.goto(link, { waitUntil: 'networkidle', timeout: 30000 });

        const filename = link
          .replace(BASE_URL, '')
          .replace(/[^\w]/g, '_') || 'home';

        await p.screenshot({
          path: `screenshots/${filename}_${vp.name}.png`,
          fullPage: true
        });

      } catch (err) {
        console.log(`❌ Error en ${link}:`, err.message);
      }

      await ctx.close();
    }
  }

  await browser.close();

  console.log('🎉 Listo! Screenshots generadas en /screenshots');
})();
