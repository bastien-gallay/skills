---
name: Skills Hub Vitrine
description: The control desk for Bastien Gallay's Claude skills — modules, status lamps, copyable install connectors.
colors:
  paper: "#F5F1E8"
  plate: "#ECE6D8"
  ink: "#17150F"
  graphite: "#3A362C"
  meta: "#494332"
  hairline: "#8B8474"
  signal: "#E8A317"
  live: "#4FA88A"
typography:
  display:
    fontFamily: 'ui-monospace, "SF Mono", "JetBrains Mono", monospace'
    fontSize: "clamp(2rem, 5vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.01em"
  headline:
    fontFamily: 'ui-monospace, "SF Mono", "JetBrains Mono", monospace'
    fontSize: "1.75rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "0"
  title:
    fontFamily: 'ui-monospace, "SF Mono", "JetBrains Mono", monospace'
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0"
  body:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0"
  label:
    fontFamily: 'ui-monospace, "SF Mono", "JetBrains Mono", monospace'
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.12em"
  data:
    fontFamily: 'ui-monospace, "SF Mono", "JetBrains Mono", monospace'
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0"
    fontFeature: '"tnum" 1'
rounded:
  sm: "2px"
  md: "4px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "32px"
  xl: "64px"
components:
  module:
    backgroundColor: "{colors.plate}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "20px"
  connector:
    backgroundColor: "{colors.plate}"
    textColor: "{colors.graphite}"
    typography: "{typography.data}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
  connector-live:
    backgroundColor: "{colors.plate}"
    textColor: "{colors.ink}"
    typography: "{typography.data}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
  led-stable:
    backgroundColor: "{colors.live}"
    size: "10px"
  led-beta:
    backgroundColor: "{colors.paper}"
    size: "10px"
  class-toggle:
    backgroundColor: "{colors.plate}"
    textColor: "{colors.meta}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  domain-tag:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.meta}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "4px 8px"
---

<!-- markdownlint-disable MD025 MD026 MD036 -- Stitch DESIGN.md format: single body H1 alongside frontmatter, the mandated **Creative North Star** / **Font** emphasis lines, and the "Do:" / "Don't:" section headings. -->

# Design System: Skills Hub Vitrine

## 1. Overview

**Creative North Star: "The Control Desk"**

The vitrine is a studio control desk, not a card grid. Every skill is a *module*
on the board, and the board has the vocabulary of an instrument: engraved labels,
signal rows, a status lamp per module, and one master command plate at the top.
The reader is a developer who lives in a terminal; the page speaks their dialect —
monospace carries anything that is *signal* (plugin names, commands, versions),
humanist sans carries anything that is *prose*. Nothing is decorative for its own
sake; each affordance earns its place at the desk.

The desk is calm by design. Boldness is spent in exactly one orchestrated place:
the install connector lights amber the moment you copy it — a jack patched, a
signal going live. Everything else stays quiet so that one moment reads. The
neutrals are *inked, not gray*: warm technical paper (`#F5F1E8`) under deep ink
(`#17150F`), with a faint amber bias so the surface feels like equipment, not an
office document. Warmth lives in the paper and the lamp, never in a tinted-white
"editorial" wash.

This system explicitly rejects the cream-and-serif editorial AI landing, the
generic same-sized card grid, purple-blue gradients, Inter / Space Grotesk, emoji
markers, and reflexive `01 / 02 / 03` section scaffolding. Order appears only
where it carries meaning — status sort (stable before beta) is the one real
ordering on the board.

**Key Characteristics:**

- Control-desk metaphor: modules, status lamps, engraved labels, install connectors.
- Monospace = signal, humanist sans = prose. A strict, honest split.
- Inked warm neutrals; amber is the single accent and the single bold moment.
- Flat and engraved at rest; the only emitted light is the amber patch on copy.
- WCAG AAA throughout; status never rides on color alone.

## 2. Colors

An inked warm-neutral field with a single amber signal lamp and one muted status green — an instrument palette, not a brand rainbow.

### Primary

- **Signal Amber** (`#E8A317`): The one accent. The status lamp glow, the install
  connector's live-patch light, focus rings, and large mono numerals. On the dark
  theme (ground `#17150F`) it reaches 8.42:1 and **may** carry large mono text; on
  the light paper it is 1.92:1 and is therefore **signal only — never text, not
  even large**. Its rarity is the entire point.

### Secondary

- **Living Green** (`#4FA88A`): A muted verdigris reserved for the *stable* status
  lamp. It is a semantic LED color, not a second decorative accent, and never
  carries text on paper (2.55:1).

### Neutral

- **Technical Paper** (`#F5F1E8`): The light-theme ground. Warm, faintly ambered,
  the surface of a well-used desk.
- **Sunken Plate** (`#ECE6D8`): The recessed surface for modules and install
  connectors — a shade darker than paper so the board reads as machined, not
  printed.
- **Deep Ink** (`#17150F`): Primary text on paper (16.19:1, AAA) and the
  dark-theme ground. Not pure black — inked.
- **Graphite** (`#3A362C`): Secondary text and intermediate surfaces (10.68:1 on
  paper, AAA). The mono command text inside connectors at rest.
- **Engraved Meta** (`#494332`): Small engraved labels, domain tags, and meta text.
  This is the *text-capable* muted color — it replaces the hairline for anything a
  reader must read. Chosen to clear AAA (≥7:1) not just on the paper ground but on
  every raised surface it sits on (module plate 7.9:1, connector seat 7.2:1); the
  softer `#565040` only cleared AAA on the ground, so labels on plates would have
  slipped to AA.
- **Hairline** (`#8B8474`): Dividers, the LED-off ring, module borders — **non-text
  only** (3.30:1, fails AAA/AA for text). If a hairline needs a label, that label
  is Engraved Meta, not this.

### Theme derivation

Both themes derive at the token layer (`:root`, `@media prefers-color-scheme`, then
`:root[data-theme=…]` overrides in both directions). Dark theme: ground = Deep Ink,
primary text = Technical Paper, sunken plate = `#201D15`, muted meta text =
`#BDB6A2` (AAA on ink and every raised surface), and Signal Amber becomes text-capable for large
mono (8.42:1). The lamp hues are identical across themes.

### Named Rules

**The Lamp-Never-Text Rule.** Signal Amber and Living Green are *emitted light*.
They fill lamps, rings, and glows — they never set body or label text on paper. On
the light theme they fail contrast for text by design; if you are tempted to write
in amber, you have mistaken the lamp for the ink.

**The Inked-Neutral Rule.** Every neutral carries a faint amber bias; none is a
pure gray. If a swatch reads as office-document gray, it is wrong — pull it back
toward the paper's warm hue.

## 3. Typography

**Display / Signal Font:** `ui-monospace, "SF Mono", "JetBrains Mono", monospace` — system monospace stacks, deliberately un-webfonted.

**Body Font:** `system-ui, -apple-system, "Segoe UI", sans-serif` — humanist system sans.

**Label / Data Font:** the same monospace, tracked and uppercased for engraved labels, `tabular-nums` for versions and commands.

**Character:** A hard, honest split — monospace is *signal*, humanist sans is
*prose*. The pairing contrasts on the mono-vs-proportional axis, never two similar
sans families. The mono carries the personality; we ship the developer's own
system mono rather than a 150 KB webfont, and say so out loud. No silent fallback.

### Hierarchy

- **Display** (700, `clamp(2rem, 5vw, 2.5rem)`, 1.05): The master command plate at
  the top — the hub name and the one install command that adds the whole
  marketplace. Ceiling held at 2.5rem; the desk states, it does not shout.
- **Headline** (600, 1.75rem, 1.15): Section plates ("Skills", "Styles").
- **Title** (600, 1.25rem, 1.2): A module's name, in mono — it is signal.
- **Body** (400, 1rem, 1.55): Skill descriptions, in humanist sans, capped at
  ~65ch. `text-wrap: pretty` to kill orphans.
- **Label** (600, 0.75rem, `letterSpacing 0.12em`, uppercase): Engraved labels and
  domain tags. Color is Engraved Meta (AAA), never Hairline.
- **Data** (500, 0.875rem, `tnum`): Install commands and versions, mono with
  tabular figures so digits and versions align down the board.

### Named Rules

**The Signal-vs-Prose Rule.** If it is a command, a plugin name, a version, or a
status, it is monospace. If it is a sentence a human reads, it is humanist sans.
There is no third font and no overlap.

**The Balanced-Title Rule.** `text-wrap: balance` on Display and Headline; test the
longest module name and the hub command at every breakpoint. A title that overflows
its plate on tablet is a failed title — reduce the clamp max or the copy, never let
it bleed.

## 4. Elevation

The desk is **flat and engraved at rest**. There are no ambient drop shadows and no
floating cards; depth is conveyed by tonal layering (paper → sunken plate) and
hairline borders, the way a real panel is machined rather than stacked. The single
exception is *emitted* light, not cast shadow: when an install connector is copied,
an amber glow radiates from it. That glow is the one elevation event on the page.

### Shadow Vocabulary

- **Patch Glow** (`box-shadow: 0 0 0 1px var(--signal), 0 0 20px -4px rgba(232,163,23,0.55)`):
  The connector's live state on copy/hover. A ring plus a soft amber bloom — light
  emitted by the patch, never a grey drop shadow beneath it.
- **Inset Seat** (`box-shadow: inset 0 0 0 1px var(--hairline)`): The resting seat
  of modules and connectors — a machined edge, not a lift.

### Named Rules

**The Emitted-Light Rule.** The board casts no shadows for depth. The only
`box-shadow` that reads as elevation is the amber patch glow, and it is *light the
instrument emits*, not gravity. Grey ambient card shadows are forbidden.

## 5. Components

For each component, lead with a short character line, then specify shape, color assignment, states, and any distinctive behavior.

### Buttons

- **Shape:** Crisp, near-square (`rounded.sm` = 2px on controls, `rounded.md` = 4px
  on plates). Instrument hardware, not soft SaaS pills.
- **Class toggle (primary control):** A segmented Skills / Styles switch on the
  sunken plate, engraved Label type in Engraved Meta; the active segment seats with
  an inset hairline and its label goes to Ink. It filters the board — it encodes a
  registry truth (class A vs B), not decoration.
- **Copy control:** Lives inside the connector (see below); on activation it flips
  to a "copied" state with an explicit text + lamp change, never color alone.

### Chips

- **Domain tag:** A small engraved Label on paper, Engraved Meta text, hairline
  seat, `rounded.sm`. Reads as a stamped legend on the module, not a colored pill.
  Never uses a lamp hue.

### Cards / Containers

- **Module (the signature container):** The card's replacement. A row on the board,
  not a floating card, and **never nested**. Corner `rounded.md` (4px); background
  Sunken Plate; Inset Seat border; internal padding `20px`. Contents in fixed
  order: status lamp · name (mono Title) · domain tag (engraved) · description
  (body sans) · install connector. A `class=style` module carries a Living-Green
  hairline on its leading edge as a **1px full seat accent** — never a thick
  side-stripe.
- **Shadow strategy:** Inset Seat at rest; no ambient shadow. See Elevation.

### Inputs / Fields

- The vitrine has no free-text inputs; its only "input" is the copy action on a
  connector. If search is added later, it inherits the connector's sunken-plate
  seat, mono Data type, and an amber focus ring (never a grey glow).

### Navigation

- Minimal. The master command plate is the header; the class toggle is the only
  persistent control. No top nav bar, no hamburger — the whole board is one screen.
  Focus is visible on every connector and control (amber ring, `:focus-visible`).

### Install Connector (signature component)

The heart of the desk. A copyable mono block — `/plugin install <name>@skills` —
seated in the plate with tabular Data type. **Resting:** Graphite mono text, Inset
Seat, a small hollow "jack" indicator. **On hover/copy:** the jack fills, the text
goes to Ink, and the Patch Glow fires — the amber signal going live, the one bold
moment on the page. **Reduced motion:** the lit state applies *instantly* (no
transition); the connector still reaches its amber state, it just doesn't animate
there. The lit state is never gated behind a transition, so it can't ship blank in
a headless render.

### Status Lamp (signature component)

Per-module LED, 10px. **Stable:** a filled Living-Green disc. **Beta:** a hollow
amber ring. Status is **never color alone** — every lamp is paired with a mono text
label (`STABLE` / `BETA`) in Engraved Meta, so a colorblind reader gets status from
shape (filled vs ring) and text, not hue.

## 6. Do's and Don'ts

### Do:

- **Do** keep Signal Amber to lamps, rings, glows, and (dark theme only) large mono
  numerals. Its rarity is the point — the Lamp-Never-Text Rule.
- **Do** verify every text token to AAA (7:1 body) in *both* themes, and against the
  raised surface it actually sits on, not just the page ground; use Engraved Meta
  (`#494332` light / `#BDB6A2` dark) for muted labels, never Hairline.
- **Do** render every module from `registry.json`. The board shows what the
  registry says; never hand-edit skill names, versions, or descriptions into the
  markup.
- **Do** back every status lamp with a shape difference (filled vs ring) *and* a
  text label, so status survives colorblindness and grayscale.
- **Do** spend the one bold moment on the install connector's patch glow, and keep
  everything else calm.
- **Do** honor `prefers-reduced-motion`: the connector reaches its lit amber state
  instantly, never gated behind a transition.
- **Do** use monospace for every signal (command, plugin name, version, status) and
  humanist sans for every sentence — the Signal-vs-Prose Rule.

### Don't:

- **Don't** write text in Signal Amber or Living Green on paper — they fail contrast
  by design; they are emitted light, not ink.
- **Don't** ship the cream-and-serif editorial AI landing, a generic same-sized card
  grid, purple-blue gradients, Inter / Space Grotesk, or emoji markers. (PRODUCT.md
  anti-references, enforced here.)
- **Don't** add reflexive `01 / 02 / 03` section numbers or a tiny tracked eyebrow
  above every section. Order appears only where it means something (status sort).
- **Don't** use a `border-left`/`border-right` colored side-stripe on modules. The
  `class=style` accent is a **1px full seat**, never a thick side rail.
- **Don't** nest modules, or float them as ambient-shadow cards. Flat, engraved,
  inset-seated — the Emitted-Light Rule.
- **Don't** cast grey drop shadows for depth. The only elevation is the amber patch
  glow.
- **Don't** silently swap in a webfont. The system mono is a deliberate, stated
  choice; if an embedded display mono is ever added, inline it and say so.
