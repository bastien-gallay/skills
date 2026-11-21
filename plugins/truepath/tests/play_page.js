// Plays a built page without a browser: every tab, every step, on a stand-in DOM.
//   node play_page.js page.html [reduced]  ->  {"tabs": n, "steps": n, "pairSteps": n, "playingOnLoad": b,
//                                               "playMarkedOnLoad": b, "html": [every innerHTML the page set]}
// It catches what the build cannot: a runtime error, and spec text reaching the page as markup.
const fs = require('fs');
const page = fs.readFileSync(process.argv[2], 'utf8');
const script = page.slice(page.indexOf('<script>') + 8, page.lastIndexOf('</script>'));
const html = [];
function node() {
  const attrs = {}, kids = [], classes = new Set();
  const n = {
    style: {}, dataset: {}, children: kids, options: [], className: '', textContent: '',
    classList: {
      toggle: (c, on = !classes.has(c)) => (on ? classes.add(c) : classes.delete(c), on),
      add: c => classes.add(c), remove: c => classes.delete(c), contains: c => classes.has(c),
    },
    setAttribute: (k, v) => { attrs[k] = String(v); }, getAttribute: k => attrs[k] ?? '',
    appendChild: c => (kids.push(c), c), addEventListener() {},
    querySelector: () => node(), querySelectorAll: () => kids,
    getTotalLength: () => 10, getPointAtLength: () => ({ x: 0, y: 0 }), closest: () => null,
  };
  let inner = '';
  Object.defineProperty(n, 'innerHTML', { get: () => inner, set: v => { inner = String(v); if (inner) html.push(inner); kids.length = 0; } });
  return n;
}
const byId = {};
const document = {
  body: node(), addEventListener() {},
  getElementById: id => (byId[id] ??= Object.assign(node(), id === 'speed' ? { options: [node()] } : {})),
  createElement: node, createElementNS: node, querySelectorAll: () => byId.tabs ? byId.tabs.children : [],
};
const env = {
  document, localStorage: { getItem: () => null, setItem() {} }, matchMedia: () => ({ matches: process.argv[3] === 'reduced' }),
  requestAnimationFrame: () => 0, cancelAnimationFrame() {}, setTimeout: () => 0, clearTimeout() {},
};
const run = new Function(...Object.keys(env), script + '\nreturn {TABS, openTab, go, nSteps, st, grid, divergence, sidesOf};');
const p = run(...Object.values(env));
const playingOnLoad = p.st.playing, playMarkedOnLoad = byId.play.classList.contains('go');
const pairTab = p.TABS.findIndex(t => t.pair);
let steps = 0, pairSteps = 0;
p.TABS.forEach((t, i) => {
  for (const view of ['detail', 'overview']) {
    p.st.view = view;
    const variants = t.case ? p.grid.sections[0].columns.map(c => c.variant) : [null];
    for (const v of variants) {
      if (v) { p.st.section = 0; p.st.minus = p.grid.baseline; p.st.plus = v; }
      p.openTab(i);
      for (let s = 0; s < p.nSteps(); s++) { p.go(s); steps++; if (i === pairTab && view === 'detail') pairSteps++; }
    }
  }
});
const parted = pairTab < 0 ? null : p.divergence(...p.sidesOf(p.TABS[pairTab]));
process.stdout.write(JSON.stringify({ parted, tabs: p.TABS.length, steps, pairSteps, playingOnLoad, playMarkedOnLoad, html }));
