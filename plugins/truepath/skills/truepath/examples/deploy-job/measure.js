// Measured time per step: runs.json is a fictitious CI log, one entry per run, already cut into steps.
// A run is cut by the time stamps of its log lines; when modules run side by side, a second counts for the step
// furthest along. Failed runs are left out and counted. Each case gets the mean of its week's runs.
const fs = require("fs");
const cases = JSON.parse(fs.readFileSync(process.env.TRUEPATH_MEASURE_IN, "utf8"));
const runs = JSON.parse(fs.readFileSync("runs.json", "utf8"));
const mean = xs => Math.round(10 * xs.reduce((a, b) => a + b, 0) / xs.length) / 10;
const out = cases.map(({ inputs }) => {
  const week = runs.filter(r => r.week === inputs.week), ok = week.filter(r => r.ok);
  const steps = {};
  for (const node of Object.keys(ok[0].steps)) steps[node] = mean(ok.map(r => r.steps[node]));
  return {
    total: mean(ok.map(r => r.duration)), n: ok.length, failed: week.length - ok.length, steps,
    basis: "measure: runs.json, a fictitious CI log; each run cut into steps by the time stamps of its log lines",
  };
});
fs.writeFileSync(process.env.TRUEPATH_MEASURE_OUT, JSON.stringify(out));
