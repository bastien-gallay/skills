// Glue, not the unit: runs src/pay.js unchanged, its collaborators replaced by doubles.
// - gateway, a stub: answers what the scenario lists, one answer per charge;
// - clock, a mock: records each wait pay asks for, and never sleeps.
// What pay decides is code; what the stub answered is the scenario, said by a `double:` basis.
const fs = require('fs');
const { pay } = require('./pay.js');

const CODE = 'code: src/pay.js';
const inputs = JSON.parse(fs.readFileSync(process.env.TRUEPATH_ORACLE_IN, 'utf8'));
const verdicts = inputs.map(({ answers, maxAttempts }) => {
  const queue = [...answers], answered = [], waits = [];
  const gateway = { charge: () => { const a = queue.shift() ?? 'timeout'; answered.push(a); return a; } };
  const clock = { sleep: ms => waits.push(ms) };
  const { outcome, attempts } = pay({ id: 'order-1', amount: 42 }, gateway, clock, maxAttempts);
  return {
    outcome, attempts, waits, answered,
    basis: {
      outcome: CODE, attempts: CODE,
      waits: `${CODE}, as the clock mock recorded what it asked`,
      answered: 'double: the gateway stub answers what the scenario lists',
    },
  };
});
fs.writeFileSync(process.env.TRUEPATH_ORACLE_OUT, JSON.stringify(verdicts));
