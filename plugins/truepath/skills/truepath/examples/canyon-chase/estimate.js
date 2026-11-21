// Seconds per step, as a cartoon would time them; nothing was measured.
const fs = require('fs');
const cases = JSON.parse(fs.readFileSync(process.env.TRUEPATH_MEASURE_IN, 'utf8'));
const out = cases.map(({ inputs: i }) => {
  let steps;
  if (i.plan === 'bomb') steps = { FUSE: 1, ZOOM: 2 };
  else if (i.plan === 'rocket') steps = { STRAP: 3, SPIN: i.fuel * 1.375 };
  else if (i.who === 'bird') steps = { EDGE: 1.5, AIR: 1, ACROSS: 1 };
  else steps = { EDGE: 3, AIR: 2, HANG: 2, BOTTOM: 1 };
  const total = +Object.values(steps).reduce((a, b) => a + b, 0).toFixed(2);
  return { total, steps, basis: 'estimate: cartoon timing, a beat per gag' };
});
fs.writeFileSync(process.env.TRUEPATH_MEASURE_OUT, JSON.stringify(out));
