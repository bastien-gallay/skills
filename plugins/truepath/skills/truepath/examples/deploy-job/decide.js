// The rule shown is the path, not a decision: every run applies the modules the merge changed, one by one, then ends.
// The time each step takes is measured (measure.js), not computed here.
exports.decide = inputs => ({
  outcome: "DONE",
  modules: inputs.modules,
  basis: { outcome: "port: a run ends once every changed module is applied", modules: "port: one pass of the loop per changed module" },
});
