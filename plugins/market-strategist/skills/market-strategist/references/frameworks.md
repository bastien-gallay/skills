# Framework Library — Market Strategist

## Table of Contents

### Well-Known Frameworks

1. [PESTEL](#pestel)
2. [Competitive Map](#competitive-map)
3. [Blue Ocean — 4 Actions Framework](#blue-ocean)
4. [Value Proposition Canvas](#vpc)
5. [Business Model Canvas](#bmc)
6. [19 Traction Channels](#traction)
7. [Growth Loop](#growth-loop)
8. [SONCAS Profile](#soncas)
9. [Argument Structure](#argument)
10. [Objection Map](#objections)
11. [Audience Profile](#audience)
12. [Message Architecture](#message)
13. [Content Channels (Thought Leadership)](#content)
14. [Porter's 5 Forces](#porter)

### Lesser-Known & Emerging Frameworks

 1. [Jobs-to-be-Done (JTBD) + Opportunity Scoring](#jtbd)
 2. [Obviously Awesome — Positioning (April Dunford)](#obviously-awesome)
 3. [Wardley Maps](#wardley)
 4. [The Mom Test (Rob Fitzpatrick)](#mom-test)
 5. [Crossing the Chasm — Segment Targeting](#chasm)
 6. [Causal Loop Diagram (Systems Thinking)](#cld)
 7. [Diffusion of Innovation Adoption Curve](#diffusion)
 8. [Narrative Positioning (StoryBrand / SB7)](#storybrand)
 9. [Ecosystem Map (Platform Strategy)](#ecosystem)
10. [Enemy Framework (Positioning through contrast)](#enemy)

---

## WELL-KNOWN FRAMEWORKS

---

## 1. PESTEL {#pestel}

**Purpose:** Scan the macro-environment for forces that will help or hinder the project.

**How to execute:**
For each of the 6 dimensions, generate 3-5 relevant factors specific to the project.
Tag each as Opportunity (O), Threat (T), or Neutral (N).

```text
PESTEL Analysis — [Project Name]

┌─────────────────┬──────────────────────────────────┬─────┐
│ Dimension       │ Factor                           │ O/T │
├─────────────────┼──────────────────────────────────┼─────┤
│ Political       │ ...                              │     │
│ Economic        │ ...                              │     │
│ Social          │ ...                              │     │
│ Technological   │ ...                              │     │
│ Environmental   │ ...                              │     │
│ Legal           │ ...                              │     │
└─────────────────┴──────────────────────────────────┴─────┘
```

**Synthesis:** Top 2 opportunities + top 2 threats. Force a choice: "Which of these
will most determine success or failure in year 1?"

---

## 2. Competitive Map {#competitive-map}

**Purpose:** Visualize the competitive landscape to reveal underserved zones.

**How to execute:**

Step 1 — List 5-10 competitors: direct, indirect, and non-consumption alternatives.

Step 2 — Choose 2 axes that matter most to the target audience (e.g., price vs. depth,
accessibility vs. specialization, speed vs. quality). These axes should create tension.

Step 3 — Place each player on the map. Identify clusters and white space.

```text
HIGH [Axis Y]
     │         ● CompetitorA    ● CompetitorB
     │
     │                    ◯ [WHITE SPACE]
     │
     │    ● CompetitorC              ● CompetitorD
LOW  └──────────────────────────────────────────▶
          LOW [Axis X]              HIGH [Axis X]
```

Step 4 — Where would the project live? Is it in a cluster (red ocean) or near white space?

**Key question:** "What would a player need to give up to move into the white space?"

---

## 3. Blue Ocean — 4 Actions Framework {#blue-ocean}

**Purpose:** Design a new value curve that escapes competition.
**Prerequisite:** Run Competitive Map first.

**How to execute:**

Step 1 — Strategy Canvas: score each competitor on 6-8 key competition factors (1-5 scale).

```text
Strategy Canvas — [Sector]

Factor          │ Comp.A │ Comp.B │ Comp.C │ Us (current) │ New Curve
────────────────┼────────┼────────┼────────┼──────────────┼──────────
[Factor 1]      │   3    │   4    │   2    │      2       │    ?
[Factor 2]      │   4    │   4    │   5    │      3       │    ?
[Factor 3]      │   2    │   1    │   2    │      1       │    ?
...
```

Step 2 — 4 Actions:

| Action | Question | Items |
| -------- | ---------- | ------- |
| **ELIMINATE** | What factors does the industry assume are necessary but add no real value? | |
| **REDUCE** | What factors should be reduced well below industry standard? | |
| **RAISE** | What factors should be elevated well above industry standard? | |
| **CREATE** | What factors have never been offered that should exist? | |

Step 3 — New Value Curve: what does a product look like that executes this 4-Actions table?
Which 2-3 factors does it dramatically overinvest in? What does it deliberately ignore?

Step 4 — Non-customer insight: who currently uses *nothing* because no product fits their need?
What would need to be true for them to become users?

---

## 4. Value Proposition Canvas {#vpc}

**Purpose:** Achieve product-market fit clarity at the level of one specific customer segment.

**How to execute:**

**Customer Profile (right side):**

```text
┌──────────────────────────────────────────────┐
│ CUSTOMER JOBS (what they're trying to do)    │
│  Functional: ...                             │
│  Social: ...                                 │
│  Emotional: ...                              │
├──────────────────────────────────────────────┤
│ PAINS (obstacles, risks, frustrations)       │
│  ...                                         │
├──────────────────────────────────────────────┤
│ GAINS (desired outcomes, benefits wanted)    │
│  ...                                         │
└──────────────────────────────────────────────┘
```

**Value Map (left side):**

```text
┌──────────────────────────────────────────────┐
│ PRODUCTS & SERVICES                          │
│  ...                                         │
├──────────────────────────────────────────────┤
│ PAIN RELIEVERS (how you address pains)       │
│  ...                                         │
├──────────────────────────────────────────────┤
│ GAIN CREATORS (how you deliver gains)        │
│  ...                                         │
└──────────────────────────────────────────────┘
```

**Fit check:** Draw explicit lines between Pain Relievers ↔ Pains, and Gain Creators ↔ Gains.
Anything unconnected on the Value Map is a feature in search of a need.

---

## 5. Business Model Canvas {#bmc}

**Purpose:** Full business model overview on one page.

```text
┌─────────────┬──────────────┬─────────────┬──────────────┬─────────────┐
│ KEY         │ KEY          │ VALUE       │ CUSTOMER     │ CUSTOMER    │
│ PARTNERS    │ ACTIVITIES   │ PROPOSITION │ RELATIONSHIPS│ SEGMENTS    │
│             │              │             │              │             │
│             ├──────────────┤             │              │             │
│             │ KEY          │             │              │             │
│             │ RESOURCES    │             ├──────────────┤             │
│             │              │             │ CHANNELS     │             │
├─────────────┴──────────────┴─────────────┴──────────────┴─────────────┤
│ COST STRUCTURE                    │ REVENUE STREAMS                   │
│                                   │                                   │
└───────────────────────────────────┴───────────────────────────────────┘
```

Fill each block with 3-5 concrete items. Then identify: which block is most uncertain?
That's where the project's biggest risk lives.

---

## 6. 19 Traction Channels {#traction}

**Purpose:** Systematically discover which acquisition channel to prioritize.
*(From "Traction" by Gabriel Weinberg & Justin Mares)*

**The 19 channels:**

1. Viral Marketing
2. Public Relations (PR)
3. Unconventional PR (stunts, stories)
4. Search Engine Marketing (SEM)
5. Social & Display Ads
6. Offline Ads
7. SEO (content, technical)
8. Content Marketing
9. Email Marketing
10. Engineering as Marketing (tools, calculators, embeds)
11. Targeting Blogs
12. Business Development (partnerships)
13. Sales (direct)
14. Affiliate Programs
15. Existing Platforms (App Store, marketplaces)
16. Trade Shows & Events
17. Offline Events & Community
18. Speaking & Thought Leadership
19. Community Building

**How to execute — Bullseye Framework:**

Step 1 — Score each channel on 2 dimensions for this specific project:

- **Reach potential** (1-5): how many target users could this realistically reach?
- **Fit with project** (1-5): does this channel match the audience's behavior and the project's resources?

Step 2 — Place in 3 rings:

```text
Outer ring:  Score < 5  → "Possible but unlikely"
Middle ring: Score 5-7  → "Worth testing"
Inner ring:  Score 8+   → "Bullseye candidates"
```

Step 3 — From the inner ring, select 1-2 channels to test first.
**Key principle:** at any stage, one channel will dominate. Find it and go deep before diversifying.

---

## 7. Growth Loop {#growth-loop}

**Purpose:** Design a self-reinforcing acquisition mechanism (vs. linear funnels).

**How to execute:**

A growth loop has 4 components:

```text
INPUT → ACTION → OUTPUT → REINVESTMENT → (back to INPUT)
```

Example — Content loop:

```text
New user finds article (INPUT)
→ Reads, gets value, shares (ACTION)
→ New visitors arrive (OUTPUT)
→ Some become contributors who write more content (REINVESTMENT)
```

**Types of growth loops:**

- Viral: users invite others as part of core use
- Content: users generate content that attracts new users
- Paid: revenue funds more acquisition
- Product: usage creates data/network effects that improve the product

**For the project:** map the most plausible loop. What's the reinvestment mechanism?
If there isn't one, the project has a funnel, not a loop — that's fine, but name it.

---

## 8. SONCAS Profile {#soncas}

**Purpose:** Map the psychological motivations of a specific decision-maker to structure a persuasive pitch.

**The 6 motivations:**

| Letter | Motivation | Profile signals | Lever |
| -------- | ----------- | ---------------- | ------- |
| **S** | Sécurité | Risk-averse, asks about guarantees, references | Proof, track record, risk mitigation |
| **O** | Orgueil | Status-conscious, wants to be seen as innovative | Recognition, exclusivity, prestige |
| **N** | Nouveauté | Excited by new tech, trends, innovation | Forward-looking vision, first-mover |
| **C** | Confort | Values ease, simplicity, low friction | Ease of adoption, support, simplicity |
| **A** | Argent | ROI-focused, budget-conscious | Numbers, savings, efficiency gains |
| **S** | Sympathie | Relationship-driven, trust-based decisions | Personal connection, shared values |

**How to execute:**

1. Profile the target decision-maker using SONCAS — rank their top 2-3 motivations.
2. For each dominant motivation, identify: what do you say? what do you show? what do you avoid?
3. Order the pitch to lead with the dominant motivation, support with secondary ones.

---

## 9. Argument Structure {#argument}

**Purpose:** Build a structured, persuasive argument for a pitch, proposal, or recommendation.

**Template — Toulmin-inspired:**

```text
CLAIM:     [What you're asserting — the ask or recommendation]

GROUNDS:   [Evidence, data, observations that support the claim]
           1. ...
           2. ...
           3. ...

WARRANT:   [Why these grounds support this claim — the logical bridge]

BACKING:   [What gives the warrant authority — precedent, expertise, analogies]

QUALIFIER: [How strong is the claim? "In most cases...", "Given that..."]

REBUTTAL:  [The strongest counter-argument, and your response to it]
```

**How to execute:** Fill all 6 elements for the user's specific situation.
Then test: "If the decision-maker only heard the CLAIM and REBUTTAL, would they still be convinced?"

---

## 10. Objection Map {#objections}

**Purpose:** Anticipate resistance and prepare responses before a high-stakes conversation.

**How to execute:**

List the 5-7 most likely objections for this specific audience. For each:

| Objection | Type | Response strategy | Pre-empt in pitch? |
| ----------- | ------ | ------------------ | -------------------- |
| "Too expensive" | Price | ROI calculation, phased approach | Yes — mention value before price |
| "Not the right time" | Urgency | Cost of inaction, window argument | Yes |
| "We tried this before" | History | What's different now | Yes |
| ... | ... | ... | ... |

**Objection types:** Price / Urgency / Trust / Complexity / History / Priority / Risk

**Key principle:** the best objection handling happens before the objection is raised.
Mark which objections to pre-empt in the pitch itself vs. hold for Q&A.

---

## 11. Audience Profile {#audience}

**Purpose:** Build a sharp, actionable picture of the target audience — beyond demographics.

**How to execute:**

```text
AUDIENCE PROFILE — [Segment Name]

WHO THEY ARE
  Role/context: ...
  Situation: ...
  
WHAT THEY'RE TRYING TO DO
  Primary job: ...
  Secondary jobs: ...
  
WHAT STOPS THEM
  Friction: ...
  Fears: ...
  
WHERE THEY LIVE (information diet)
  Platforms: ...
  Trusted voices: ...
  Content formats: ...
  
WHAT THEY ALREADY BELIEVE
  About this problem: ...
  About existing solutions: ...
  
THE SENTENCE THEY'D USE TO DESCRIBE THEIR NEED
  "I just want to..."
```

Build 1-3 profiles max. More than that, the strategy becomes unfocused.

---

## 12. Message Architecture {#message}

**Purpose:** Define a coherent communication hierarchy for consistent messaging across channels.

**How to execute:**

```text
MESSAGE ARCHITECTURE — [Project Name]

CORE MESSAGE (one sentence — the single thing you want people to remember)
  "[Project] is the [category] for [audience] who [need], unlike [alternative]."

PRIMARY MESSAGES (3 — support the core, each for a different audience motivation)
  1. [Message for motivation A]
  2. [Message for motivation B]
  3. [Message for motivation C]

PROOF POINTS (evidence for each primary message)
  1. → [data point / story / example]
  2. → [data point / story / example]
  3. → [data point / story / example]

TONE ATTRIBUTES (3 adjectives that define HOW you say things)
  [Adj 1] / [Adj 2] / [Adj 3]

WHAT WE NEVER SAY
  [Words, claims, or frames to avoid — and why]
```

---

## 13. Content Channels (Thought Leadership) {#content}

**Purpose:** Define where and how to communicate expertise for non-commercial or personal branding goals.

**How to execute:**

Step 1 — Map audience information consumption habits (use Audience Profile).

Step 2 — Score content channel options:

| Channel | Audience fit | Effort | Reach | Durability | Priority |
| --------- | ------------- | -------- | ------- | ------------ | ---------- |
| LinkedIn articles | | | | | |
| Newsletter | | | | | |
| Speaking at events | | | | | |
| Podcast appearances | | | | | |
| Technical blog | | | | | |
| Open-source contribution | | | | | |
| Community leadership | | | | | |
| Short-form (Twitter/X, Mastodon) | | | | | |

Step 3 — Choose 1 primary channel (deep consistency) + 1 distribution channel (repurpose).
**Key principle:** one channel mastered > three channels abandoned.

Step 4 — Define a sustainable content rhythm: what can be produced consistently without burning out?

---

## 14. Porter's 5 Forces {#porter}

**Purpose:** Analyze the structural attractiveness of a market or sector.

```text
                    [THREAT OF NEW ENTRANTS]
                           ↓
[SUPPLIER POWER] → [COMPETITIVE RIVALRY] ← [BUYER POWER]
                           ↑
                  [THREAT OF SUBSTITUTES]
```

| Force | Key questions | Rating (Low/Med/High) | Impact |
| ------- | ------------- | ---------------------- | -------- |
| **Competitive rivalry** | How many players? How differentiated? Price wars? | | |
| **Threat of new entrants** | Barriers to entry? Capital requirements? Brand loyalty? | | |
| **Supplier power** | How many suppliers? Switching costs? Unique inputs? | | |
| **Buyer power** | How many buyers? Switching costs? Price sensitivity? | | |
| **Threat of substitutes** | Alternative ways to solve the same problem? | | |

**Synthesis:** Overall attractiveness rating + the 1-2 forces that dominate this sector.

---

---

## LESSER-KNOWN & EMERGING FRAMEWORKS

---

## 15. Jobs-to-be-Done (JTBD) + Opportunity Scoring {#jtbd}

**Origin:** Clayton Christensen / Tony Ulwick (Outcome-Driven Innovation)
**Purpose:** Discover what customers are *actually* hiring a product to do — often different
from what the product thinks it does.

**Core insight:** People don't buy products; they "hire" them to make progress in their lives.
The job is stable; the solutions that fulfill it change.

**How to execute:**

Step 1 — Identify the Job Statement:

```text
When [SITUATION], I want to [MOTIVATION / JOB], so I can [DESIRED OUTCOME].
```

Step 2 — List the desired outcomes (what "success" looks like from the customer's perspective).
These are the metrics the customer uses to measure progress. Format: verb + object + context.

Step 3 — Opportunity Score each outcome:

```text
Opportunity Score = Importance + max(Importance - Satisfaction, 0)
```

| Desired Outcome | Importance (1-10) | Current Satisfaction (1-10) | Opportunity Score |
| --------------- | ----------------- | --------------------------- | ----------------- |
| ...             |                   |                             |                   |

Scores > 12: **Underserved opportunities** (high importance, low satisfaction) → focus here.
Scores < 6: **Over-served** → don't invest, reduce instead.

Step 4 — Cluster high-opportunity outcomes. This cluster defines the job segment to target.

**Why it's powerful:** It reveals what to build before you know how to build it.
More stable than persona-based analysis (jobs don't change; demographics do).

---

## 16. Obviously Awesome — Positioning (April Dunford) {#obviously-awesome}

**Origin:** April Dunford, *Obviously Awesome* (2019)
**Purpose:** Nail positioning by working from competitive context, not product features.

**Core insight:** Positioning is not a tagline. It's the context you set in a customer's mind
before they evaluate you. Wrong context → confused customers → failed sales.

**5-component positioning framework:**

```text
1. COMPETITIVE ALTERNATIVES
   What would customers do if your product didn't exist?
   (This defines your real competition — often not who you think.)

2. UNIQUE ATTRIBUTES
   What features/capabilities do you have that alternatives lack?
   (Only list things that are genuinely differentiated — not "better," but *different.*)

3. VALUE (not features)
   For each unique attribute: what value does this create for the customer?
   The bridge: attribute → "which means that" → value.

4. TARGET CUSTOMER CHARACTERISTICS
   Which customers value this the most?
   (Not demographics — identify the *characteristic* that makes them care.)

5. MARKET FRAME OF REFERENCE
   What category should you position in, and what context should you set?
   Options: existing category / re-segmented category / new category / different game entirely
```

**How to execute:** Fill all 5 components, then write a positioning statement:
> "[Product] is the [market category] that [unique value] for [target customer]
> who [characteristic], unlike [alternative] which [limitation]."

**Key question:** "Are we choosing the frame of reference that makes our strengths obvious,
or are we competing in a frame that makes us look weaker than we are?"

---

## 17. Wardley Maps {#wardley}

**Origin:** Simon Wardley
**Purpose:** Visualize strategic landscape by mapping components along two axes:
visibility to the user (y-axis) and evolutionary stage (x-axis).

**Evolutionary stages (x-axis):**

```text
Genesis → Custom-built → Product/rental → Commodity/utility
(novel,     (bespoke,      (standardized,    (invisible,
 uncertain)  expensive)     competitive)      cheap)
```

**How to execute (simplified):**

Step 1 — List the components that make up the value chain (user needs → activities → resources).

Step 2 — Place each on the map:

```text
HIGH visibility ↑
(user-facing)   │  [User Need]
                │        ↓
                │  [Component A]    [Component B]
                │                        ↓
LOW visibility  │             [Component C — commodity]
                └──────────────────────────────────────▶
              Genesis    Custom    Product    Commodity
```

Step 3 — Identify strategic insights:

- What's in Genesis that could become a differentiator?
- What's still Custom-built that should be commoditized (buy, don't build)?
- Where are competitors investing? Where is the map moving?

**Why it's powerful:** Forces explicit thinking about *evolution* — what's a differentiator today
may be a commodity in 2 years. Reveals where to invest vs. where to harvest.

---

## 18. The Mom Test {#mom-test}

**Origin:** Rob Fitzpatrick, *The Mom Test* (2013)
**Purpose:** Validate (or invalidate) business assumptions through conversations that can't be faked.

**Core insight:** Most user interviews produce false positives. People are polite.
You need to design questions that even your mom (who loves you and wants you to succeed)
can't answer dishonestly.

**Rules:**

1. Talk about their life, not your idea.
2. Ask about specific past behavior, not hypothetical future behavior.
3. Listen for concrete commitments (money, time, introductions), not compliments.

**Bad questions vs. good questions:**

| Bad (leading, hypothetical) | Good (specific, behavioral) |
| ---------------------------- | ---------------------------- |
| "Would you use a tool that does X?" | "How do you currently handle X?" |
| "Do you think this is a problem?" | "When did this last cause you a real issue?" |
| "How much would you pay for this?" | "Have you tried to solve this? What did you try?" |

**How to execute:** For the user's project, generate 5-7 "Mom Test compliant" interview questions.
Then: what would a positive signal look like? What would a disqualifying signal look like?

---

## 19. Crossing the Chasm — Segment Targeting {#chasm}

**Origin:** Geoffrey Moore, *Crossing the Chasm* (1991)
**Purpose:** Identify which customer segment to focus on to cross from early adopters to mainstream.

**Adoption curve:**

```text
Innovators → Early Adopters → [CHASM] → Early Majority → Late Majority → Laggards
   2.5%          13.5%                      34%              34%            16%
```

**The chasm:** Early adopters buy vision; the early majority buys proven solutions.
Most products die in the chasm trying to serve everyone.

**Beachhead strategy:**

1. Choose ONE specific vertical/segment in the Early Majority — small enough to dominate, large enough to matter.
2. Become the obvious leader there before expanding.
3. Use that win as a reference to enter adjacent segments.

**How to execute:**
Step 1 — Map current users: which part of the curve are they on?
Step 2 — Identify 3-5 potential beachhead segments. For each: Who? Compelling reason to buy? Whole product possible?
Step 3 — Score segments: market size × pain intensity × reachability × reference value.
Step 4 — Pick one. Define what "winning" looks like.

---

## 20. Causal Loop Diagram (Systems Thinking) {#cld}

**Origin:** Jay Forrester / Donella Meadows
**Purpose:** Model the feedback dynamics in a market — find leverage points, avoid unintended consequences.

**Two types of loops:**

- **Reinforcing (R):** growth feeds growth (or decline feeds decline). Virtuous/vicious cycles.
- **Balancing (B):** self-correcting mechanisms. Limits to growth.

**Notation:**

```text
A ──(+)──▶ B    A increases → B increases
A ──(-)──▶ B    A increases → B decreases
```

**How to execute (simplified):**

Step 1 — Identify 4-6 key variables in the system (market adoption, trust, price, network size, etc.)

Step 2 — Draw the causal relationships between them, noting + or - polarity.

Step 3 — Identify the dominant loops:

- What's the main growth engine (R loop)?
- What will eventually limit growth (B loop)?
- Where is the time delay that creates oscillation?

**Why it's powerful:** Reveals why a seemingly good strategy backfires, or why growth stalls
despite strong early traction. Especially useful for platform/marketplace/community projects.

---

## 21. Diffusion of Innovation Adoption Curve {#diffusion}

**Origin:** Everett Rogers (1962)
**Purpose:** Design messaging and channels for each stage of adoption, not one-size-fits-all.

| Segment | % | Profile | What they need to hear | Where to reach them |
| --------- | --- | --------- | ---------------------- | ------------------- |
| Innovators | 2.5% | Tech enthusiasts, risk-tolerant | "Be first, explore" | GitHub, Discord, conferences |
| Early Adopters | 13.5% | Visionaries, opinion leaders | "Strategic advantage" | Blogs, LinkedIn, referrals |
| Early Majority | 34% | Pragmatists, need proof | "Everyone like you uses this" | Case studies, reviews, word-of-mouth |
| Late Majority | 34% | Skeptics, need safety | "You'll be left behind" | Mainstream media, peer pressure |
| Laggards | 16% | Traditionalists | Usually not worth targeting | — |

**How to execute:** Identify which segment is the current target. Design messaging and channel
strategy specifically for that segment. Don't mix messages — Innovators are repelled by
"social proof" messaging; Early Majority is repelled by "be first" messaging.

---

## 22. Narrative Positioning — StoryBrand / SB7 {#storybrand}

**Origin:** Donald Miller, *Building a StoryBrand* (2017)
**Purpose:** Structure communication so the customer is the hero, not the product.

**Core insight:** Most brands talk about themselves. Customers only care about their own story.
Position your product as the **Guide**, not the Hero.

**SB7 Framework:**

```text
1. CHARACTER    The customer — who are they, what do they want?
2. PROBLEM      External (practical) / Internal (emotional) / Philosophical (moral)
3. GUIDE        Your brand — empathy + authority (you've been there / you've helped others)
4. PLAN         Simple 3-step plan that makes success feel achievable
5. CALL TO ACTION  Direct ("Buy now") + transitional ("Download the guide")
6. AVOIDING FAILURE  What's at stake if they don't act?
7. ACHIEVING SUCCESS  The life they want after using your product
```

**How to execute:** Fill each of the 7 elements for the project. Then write a one-paragraph
"BrandScript" that weaves all 7 together. Test: does it make the customer feel like the hero?

---

## 23. Ecosystem Map (Platform Strategy) {#ecosystem}

**Origin:** Platform strategy / network economics literature
**Purpose:** Map all actors in the value ecosystem — producers, consumers, partners, enablers —
and identify who creates value for whom.

**How to execute:**

Step 1 — List all actor types involved (users, contributors, partners, regulators, complementors).

Step 2 — Map value exchanges between them:

```text
[Actor A] ──── [value/data/money] ────▶ [Actor B]
              ◀──── [value/data/money] ────
```

Step 3 — Identify:

- **Core interaction:** the fundamental exchange the platform enables
- **Network effects:** does adding more of Actor A increase value for Actor B? (and vice versa?)
- **Bottlenecks:** where does value creation get blocked?
- **Missing actors:** who should be in this ecosystem but isn't yet?

**Why it's powerful:** Reveals multi-sided market dynamics invisible in linear business models.
Essential for community, platform, open-source, and marketplace projects.

---

## 24. Enemy Framework (Positioning through Contrast) {#enemy}

**Origin:** Various — popularized in brand strategy (linked to Zag by Marty Neumeier)
**Purpose:** Define positioning by naming what you're *against*, not just what you're *for*.
Sharp contrast creates memorable, defensible positions.

**Core insight:** The brain remembers contrast. "We're different because X" is weak.
"We exist because [incumbent approach] is broken, and here's how" is memorable.

**How to execute:**

Step 1 — Name the enemy. Not a competitor, but an *approach*, a *convention*, a *broken assumption*.
Examples: "complexity for its own sake", "one-size-fits-all solutions", "trading speed for quality"

Step 2 — Articulate the manifesto:

```text
WE BELIEVE [current broken approach] is wrong because [specific reason].
INSTEAD, we believe [your alternative belief].
THAT'S WHY [product/project] [does what it does differently].
```

Step 3 — Test for authenticity: does this enemy actually show up in your product decisions?
If you say you're against complexity but your product has 47 menu items, the frame is hollow.

Step 4 — Use the enemy framing to filter: every feature, every message, every partnership —
does it fight the enemy or reinforce it?

**Why it's powerful:** Gives the audience someone to root for (and against). Creates community
around shared beliefs. Especially effective for non-commercial and mission-driven projects.
