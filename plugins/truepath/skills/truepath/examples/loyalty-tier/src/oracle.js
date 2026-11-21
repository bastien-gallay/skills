// Glue between truepath and tier.js. It runs two ways:
// - under build.py (TRUEPATH_ORACLE_IN set): reads the scenarios' inputs, writes one verdict each;
// - on its own (`node src/oracle.js`): replays the exported cases.json as a regression suite.
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { tier } = require('./tier.js');

const NODE = { gold: 'GOLD', silver: 'SILVER', bronze: 'BRONZE' }; // the node each tier ends on

if (process.env.TRUEPATH_ORACLE_IN) {
  const inputs = JSON.parse(fs.readFileSync(process.env.TRUEPATH_ORACLE_IN, 'utf8'));
  const verdicts = inputs.map(({ points }) => {
    const t = tier(points);
    return { tier: t, outcome: NODE[t], basis: { tier: 'code: src/tier.js', outcome: 'defined by this glue' } };
  });
  fs.writeFileSync(process.env.TRUEPATH_ORACLE_OUT, JSON.stringify(verdicts));
} else {
  const { cases } = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'cases.json'), 'utf8'));
  for (const c of cases) assert.deepStrictEqual({ tier: tier(c.inputs.points) }, c.expected, c.name);
  console.log(`${cases.length} cases hold`);
}
