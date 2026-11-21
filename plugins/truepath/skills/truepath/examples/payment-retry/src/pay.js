// The unit: charge an order, retry a timeout after a wait that doubles, give up after `maxAttempts`.
// Its two collaborators come from outside: the gateway that charges, the clock that waits.
function pay(order, gateway, clock, maxAttempts = 3) {
  for (let attempt = 1; ; attempt++) {
    const answer = gateway.charge(order.id, order.amount);
    if (answer === 'ok') return { outcome: 'PAID', attempts: attempt };
    if (answer === 'declined') return { outcome: 'DECLINED', attempts: attempt };
    if (attempt === maxAttempts) return { outcome: 'GAVE_UP', attempts: attempt };
    clock.sleep(200 * 2 ** (attempt - 1));
  }
}

module.exports = { pay };
