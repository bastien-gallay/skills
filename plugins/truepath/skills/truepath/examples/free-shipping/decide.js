// Port of a rule under discussion: shipping is free once the basket reaches 50.
// Two questions are open: does exactly 50 count, and is the coupon taken off before the test?
function decide({ inclusive, afterCoupon, basket, coupon }) {
  const tested = afterCoupon ? basket - coupon : basket;
  const free = inclusive ? tested >= 50 : tested > 50;
  return { tested, shipping: free ? 'free' : '4.90', outcome: free ? 'FREE' : 'PAID',
    basis: { tested: 'port: decide.js', shipping: 'port: decide.js' } };
}
if (typeof module !== 'undefined') module.exports = { decide };
