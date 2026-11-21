// Cartoon physics, ported by hand: nothing here runs in a real canyon.
// A plan backfires on whoever made it. A rocket spins while it has fuel, then meets the wall.
// Past the edge, a runner stays up as long as it does not look down.
function decide({ who, plan, fuel, looksDown }) {
  if (plan === 'bomb') return { outcome: 'BOOM', ends: 'blown up', basis: { ends: 'port: the fuse is always shorter than planned' } };
  if (plan === 'rocket') return { outcome: 'WALL', ends: `into the wall, after ${fuel} spins`, spins: fuel,
    basis: { ends: 'port: a rocket spins until its fuel runs out' } };
  if (looksDown) return { outcome: 'BOTTOM', ends: 'far below', basis: { ends: 'port: you fall only once you look down' } };
  return { outcome: 'ACROSS', ends: `${who === 'bird' ? 'the bird' : 'the hunter'} got across`,
    basis: { ends: 'port: who never looks down never falls' } };
}
if (typeof module !== 'undefined') module.exports = { decide };
