// The code under simulation: which loyalty tier a number of points gives.
function tier(points) {
  if (points >= 1000) return 'gold';
  if (points >= 500) return 'silver';
  return 'bronze';
}
module.exports = { tier };
