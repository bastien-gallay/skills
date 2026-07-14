# Product

## Register

brand

## Users

Developers who use Claude Code and browse skills to install. Their context is a
terminal: they read `plugin.json`, run `/plugin install`, and judge a tool by how
honestly it presents itself. They arrive at the vitrine (the hub's showcase page,
`docs/index.html`, served by GitHub Pages) to answer one question fast — *what is
here, and how do I get it?* They scan; they do not read.

## Product Purpose

The hub `bastien-gallay/skills` is a **meta-marketplace and registry** for the
Claude skills the maintainer publishes — each skill lives in its own
independently-versioned repo; the hub aggregates, never vendors. The vitrine
makes those modules **discoverable and installable at a glance**: name, class
(skill vs style), status, domain, and a copyable install command.

Success = a visitor lands, finds the module they want, copies its install command,
and leaves — in one glance, with no friction. The page is **install-first**; its
craft is not decoration but the trust signal that makes the maintainer's work
worth installing. `registry.json` is the single source of truth — the page renders
from it and never redefines skill data by hand.

## Brand Personality

**Instrument, honest, calm.** The governing metaphor is a *centrale* — a control
panel / patchboard, not a card grid. Each skill is a *module* on a board with a
status LED and an install connector. The voice speaks the vocabulary of the
instrument: engraved labels, signal rows, monospace for anything that is "signal"
(commands, plugin names). It is confident without shouting: boldness is spent in
exactly one orchestrated place (the install patch lighting up on copy), and
everything else stays quiet. Honesty is a value, not a pose — system monospace
stacks over a silent 150 KB webfont, real registry data over hand-tuned copy.

## Anti-references

- **The cream + serif + terracotta "editorial-warm" AI landing.** This is inked
  warm paper + **monospace** + an amber signal lamp — an instrument world, not a
  magazine.
- **Generic card grid.** Same-sized icon-heading-text cards repeated endlessly.
  Modules on a board, not cards.
- **Purple-blue gradients, Inter / Space Grotesk, emoji markers.** None of it.
- **Numbered section scaffolding (01 / 02 / 03) by reflex.** Numbers/markers only
  when order carries real meaning (status sort is the only real ordering here).
- **Dispersed animation.** No entrance-reveal on every section; one orchestrated
  motion moment, nothing else.

## Design Principles

- **Registry is truth.** The page renders from `registry.json`; it never
  duplicates or hand-edits skill data. What the registry says, the board shows.
- **Speak the instrument.** Every affordance earns its place in the control-panel
  metaphor — LEDs, engraved labels, connectors, signal rows. Metaphor is
  structure, not skin.
- **Spend boldness once.** One orchestrated moment (the install patch lighting on
  copy). Calm everywhere else; risk concentrated, not sprinkled.
- **Honest materials.** System monospace stacks, real data, no silent fallbacks or
  decorative weight. If it costs the reader, it must earn its keep.
- **One glance to install.** Every layout decision serves discover → identify →
  copy. Craft is the trust signal, never the obstacle.

## Accessibility & Inclusion

- **WCAG AAA target.** Body text ≥7:1 against its ground; large text ≥4.5:1. The
  inked-neutral palette (warm paper / deep ink) and the amber signal must all be
  verified against this bar, in both light and dark themes — push body ink toward
  the dark end of the ramp rather than settling for elegant-but-faint gray.
- **Status never by color alone** (WCAG 1.4.1). Stable vs beta LEDs carry a
  shape/label backup (filled vs hollow ring, text label), so colorblind users read
  status without relying on the amber/green hue.
- **Reduced motion is non-negotiable.** `prefers-reduced-motion: reduce` disables
  the patch-lighting transition — the connector reaches its lit state instantly,
  never gated behind an animation that could leave content blank.
- **Visible focus** on every connector and copy control; copy buttons expose a
  clear state change on activation.
