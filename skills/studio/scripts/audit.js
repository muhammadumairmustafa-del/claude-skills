// Paste/eval in the rendered page (e.g. browser pane javascript_tool, or Playwright page.evaluate).
// Returns a compact report: contrast failures, horizontal overflow, small touch targets,
// unlabeled controls, images without alt, fonts actually in use.
(() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p[3] ?? 1 }; };
  const lum = ({ r, g, b }) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const bgOf = el => { // walk up until an opaque background; ignores images/gradients (flagged as 'unknown')
    for (let n = el; n; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.backgroundImage !== 'none') return null;
      const c = parse(s.backgroundColor); if (c && c.a > 0.9) return c;
    }
    return { r: 255, g: 255, b: 255, a: 1 };
  };
  const visible = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.opacity !== '0'; };
  const label = el => (el.id ? el.tagName.toLowerCase() + '#' + el.id : el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '')) + ' "' + (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 30) + '"';

  const contrast = [], unknownBg = []; const seen = new Set();
  for (const el of document.querySelectorAll('body *')) {
    if (!visible(el)) continue;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    const s = getComputedStyle(el); const fg = parse(s.color); const bg = bgOf(el);
    if (!bg) { if (unknownBg.length < 5) unknownBg.push(label(el)); continue; }
    const size = parseFloat(s.fontSize), bold = parseInt(s.fontWeight) >= 700;
    const need = size >= 24 || (bold && size >= 18.66) ? 3 : 4.5;
    const r = ratio(fg, bg);
    const key = s.color + s.backgroundColor + need;
    if (r < need && !seen.has(key)) { seen.add(key); contrast.push(`${r.toFixed(2)}:1 (need ${need}) ${label(el)}`); }
  }

  const vw = document.documentElement.clientWidth;
  const overflow = [...document.querySelectorAll('body *')].filter(el => visible(el) && el.getBoundingClientRect().right > vw + 1 && getComputedStyle(el).position !== 'fixed').slice(0, 8).map(label);

  const interactive = [...document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,[role=button],[tabindex]:not([tabindex="-1"])')].filter(visible);
  const small = interactive.filter(el => { const r = el.getBoundingClientRect(); return (r.width < 44 || r.height < 44) && !(el.tagName === 'A' && getComputedStyle(el).display === 'inline'); }).slice(0, 10).map(el => { const r = el.getBoundingClientRect(); return `${Math.round(r.width)}×${Math.round(r.height)} ${label(el)}`; });
  const unnamed = interactive.filter(el => !(el.innerText || '').trim() && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby') && !el.title && !(el.labels && el.labels.length) && !el.querySelector('img[alt]:not([alt=""])')).slice(0, 10).map(label);
  const noAlt = [...document.images].filter(i => !i.hasAttribute('alt')).slice(0, 10).map(i => i.src.split('/').pop());
  const fonts = [...new Set([...document.querySelectorAll('body *')].filter(visible).map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim()))];
  const h1 = document.querySelectorAll('h1').length;

  return {
    viewport: `${vw}×${innerHeight}`, h1Count: h1, fontsInUse: fonts,
    contrastFailures: contrast.slice(0, 15), unknownBackground: unknownBg,
    horizontalOverflow: overflow, smallTargets: small, unnamedControls: unnamed, imagesMissingAlt: noAlt,
    reducedMotionCSS: [...document.styleSheets].some(ss => { try { return [...ss.cssRules].some(r => r.conditionText && r.conditionText.includes('prefers-reduced-motion')); } catch { return false; } }),
  };
})();
