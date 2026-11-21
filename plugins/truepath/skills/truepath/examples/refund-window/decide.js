// Port of a toy rule: an order can be refunded up to and including day 30 after delivery.
// Before the fix the check used `<` and refused a request made on day 30.
function decide({ fix, days }) {
  const inWindow = fix ? days <= 30 : days < 30;
  return { inWindow, outcome: inWindow ? 'REFUND' : 'CREDIT',
    basis: { inWindow: 'port: decide.js' } };
}
if (typeof module !== 'undefined') module.exports = { decide };
