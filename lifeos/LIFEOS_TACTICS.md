# LifeOS Tactical Manual

**Version:** 2.1
**Last Updated:** 2026-01-15
**Document Type:** Tactics (changes often)

This document contains **what to actually do** in real situations: playbooks, checklists, decision trees, and situational responses. It complements LIFEOS_SPEC.md (principles) and LIFEOS_OPS.md (infrastructure).

**Key distinction:**
- SPEC states **what must happen**
- TACTICS explains **how to make it happen**

---

## Tactics Governance Rules

1. **A tactic may exist only if it was created to solve a real failure.** No speculative tactics.

2. **Promotion rule:** If a tactic is used ≥3 times successfully → consider promoting a distilled rule into SPEC.

3. **Deletion rule:** If a tactic hasn't been used in 60–90 days → archive or delete.

4. **Constraint:** Tactics may contradict preferences but must never contradict SPEC invariants.

**Purpose:** Keep the system lean over years. Tactics accumulate operational wisdom; they don't become bloat.

---

## Frequency Tags

Tactics are tagged by usage frequency:

| Tag | Meaning |
|-----|---------|
| `[DAILY]` | Execute every day |
| `[WEEKLY]` | Execute during weekly review |
| `[WHEN FRAGILE]` | Use when Day State is YELLOW/RED or Friction ≥ 3 |
| `[EMERGENCY]` | Rare, high-stakes situations only |

---

## Index of Failure Modes

**Quick lookup: Common failure → Tactic to use**

| Failure | Go To |
|---------|-------|
| Missed training week | Pillar 2 → Session Hierarchy, Drift Detection |
| Anxiety spike / overload | Pillar 1 → Daily OS Section A-E |
| Capital stagnation | Pillar 3 → Capital Failure Modes, Intervention Playbook |
| Writing avoidance | Pillar 6 → Output Intervention Playbook (72h protocol) |
| Social withdrawal | Pillar 5 → Relationship Drift Detection, Critical intervention |
| Learning streak broken | Pillar 4 → Learning Intervention Playbook |
| Ego-driven training | Pillar 2 → Identity Guardrails |
| Relationship ambiguity | Pillar 5 → Intuition Handling (in SPEC), Exit Criteria |
| Essay not distributed | Pillar 6 → Essay Launch Protocol (Social Distribution) |
| Content bank depleted | Pillar 6 → Social Metrics Check, extraction workflow |
| Sleep collapse | Pillar 1 → Daily OS Section D, Medication Context |
| Pre-mortem triggered | SPEC → Pre-Mortem Trigger section |

---

## Deep Work Sessions — Tactical

### When to Use

Deep work sessions are for substantial, focused work on a single pillar topic. Use when:
- Task requires 1-2+ hours of focused execution
- External data needs processing (CRM, spreadsheets, exports)
- Complex analysis or planning required
- Multiple sub-tasks need orchestration

### Session Initiation

**Command:** "Deep work session on [topic]"

**Response pattern:**
1. Declare focus and duration
2. Set distraction protocol
3. Create todo list for session
4. Import artifacts if needed
5. Execute

### Artifacts Workflow

**Location:** `lifeos/artifacts/`

**Pattern:** Import → Work → Export → Delete

| Phase | Action |
|-------|--------|
| Import | Paste external data into `artifacts/[topic]-[date].md` |
| Work | Process, triage, analyze, generate actions |
| Export | Push changes to external systems (CRM, sheets, etc.) |
| Delete | Remove artifact file when complete |

**Rules:**
- One artifact per session topic
- Delete artifacts at session end
- Never store credentials in artifacts
- Git-ignored by default

### Focus Protection

**Distraction protocol:** If something surfaces for another pillar during deep work:
1. Note it briefly in handoff.openLoops
2. Return immediately to session focus
3. Do NOT context-switch

**Exception:** P1 Health signals override all deep work. If Day State degrades to RED, pause session.

### Session Closure

1. Export all changes to external systems
2. Confirm exports applied
3. Delete artifact files
4. Update `today.deepWork.completed` in current-week.json
5. **Update session-log.md** (append entry)
6. **Update handoff in current-week.json** (see OPS.md § Session End)

**Rule:** Every session — morning, evening, checkin, weekly, ad-hoc — must update session-log.md and current-week.json handoff before closing. No exceptions.

---

## Pillar 1: Health & Nervous System — Tactical `[DAILY]`

### Daily Operating System

**A) MORNING CHECK (Baseline Calibration)**
- Read last night's sleep data (duration + interruptions)
- Read HRV and RHR (note trend context)
- Classify Day State:
  - **GREEN** = stable baseline
  - **YELLOW** = mild strain signal(s)
  - **RED** = dysregulation / overload signal(s)

**B) DAY PLAN RULES**
| Day State | Action |
|-----------|--------|
| GREEN | Normal plan, protect evening routine |
| YELLOW | Reduce optional load 20-40%; prioritize recovery |
| RED | Reduce load 50%+; remove intensity; recovery is primary |

**C) STIMULUS BUDGET**
If arousal high or sleep poor: reduce social stimulation, complex decisions, meeting length, conflict emails, late-night screens.

**D) EVENING SHUTDOWN**
- Clean shutdown ritual prevents "late completion drift"
- Hard boundary prevents "just one more thing" escalation
- If day went off track: do NOT catch up at night; repair tomorrow

**E) DAILY LOGGING (Minimum Viable)**
Even if tired: record single sentence about state + one adjustment. Prevents silent drift.

### Weekly Operating System

1. Review 7-day trends: sleep, HRV, RHR, mood, load
2. Identify leading indicators of drift (earliest signals)
3. Decide ONE structural change to protect stability
4. Set Recovery Anchor: one deliberate downshift block, one low-stimulus window
5. Audit calendar load: meetings, buffers, context switches
6. Pre-commit to constraints: bedtime boundary, no back-to-back intensity if sleep deteriorates

**Output must be explicit:** what worked, what failed, what changes, what gets reduced/removed.

**Mandatory Question:** "Did I interpret a nervous-system signal as a character flaw this week?"

### Medication Context (Concerta) `[WHEN FRAGILE]`

- Medication is a capacity stabiliser, not a performance amplifier
- If HRV drops or sleep degrades, assume interaction effects first
- Never stack: medication + sleep deprivation + emotional load

**Rule:** When in doubt, reduce cognitive load before adjusting dosage or expectations.

### Public Composure Rule `[EMERGENCY]`

If emotion surfaces in public or professional contexts:
1. Pause
2. Breathe
3. Continue calmly when ready
4. No post-hoc self-judgment
5. No compensatory behavior afterward

**Interpretation:** This is earned gravity, not weakness. Leaders who care and remain composed increase trust.

### Temporary Identity Statement

"I am in a deliberate integration phase. Stability now compounds everything later."

This replaces any implicit pressure to "immediately be onto the next great thing."

---

## Pillar 2: Training — Tactical `[DAILY]`

### Daily Training Protocol

**Before any training decision, query Pillar 1 status:**

| Day State | Training Action |
|-----------|-----------------|
| GREEN | Execute planned session, no extra intensity, stop while capable |
| YELLOW | Downgrade intensity OR shorten duration, strength optional |
| RED | No intensity, recovery/rest only, restraint IS training identity |

**Session Rules:**
- Warm-up mandatory
- Stop at first sharp pain
- No "just one more rep"
- End feeling under-reached, not spent

### Session Hierarchy (When Fatigued) `[WHEN FRAGILE]`

When fatigue or time pressure exists, prioritize in this order:
1. **Aerobic base (Z1/Z2)** — Never remove
2. **Strength** — Reduced volume acceptable
3. **Moderate intensity (Z3)** — Can reduce
4. **High intensity (Z4)** — First to remove

**Rule:** VO₂ work is optional under fatigue. Aerobic base is not.

### Mechanical Load Management

**Key insight:** Cardiovascular load ≠ mechanical load. This system deliberately separates them.

**Mechanical Load Sources:**
- Running (impact, eccentric stress)
- Heavy lifting (joint/tendon stress)

**Mechanical Load Controls:**
- Elliptical for Z2/Z3 volume
- Row/bike erg for VO₂ work when needed
- Gradual reintroduction of running
- Long runs capped and progressed deliberately

**Rule:** Increase cardiovascular volume faster than impact volume. If impact stress rises faster than tissue adaptation → injury risk.

### Identity Guardrails (Anti-Overreach) `[WHEN FRAGILE]`

This system is vulnerable to ego-driven escalation.

**Watch for:**
- Desire to "test fitness"
- Urge to add extra intensity
- Discomfort with easy days
- Interpreting fatigue as weakness
- Romanticising suffering

**Correct identity statement:** "I train to become inevitable, not impressive."

### Recovery Is Not Optional (Binding)

Recovery modalities are treated as active training inputs, not accessories.

- **Sauna** = cardiovascular and plasma volume adaptation
- **Cold** = autonomic balance and inflammation control
- **Sleep** = primary adaptation window

**Rule:** If recovery compliance drops, training load must drop.

### VO₂max: Supporting Metric Only

VO₂max is tracked contextually, not operationally.

**Use VO₂max to:**
- Confirm aerobic engine adequacy
- Monitor efficiency trends
- Detect regression under excessive fatigue

**Do NOT use VO₂max to:**
- Justify intensity increases
- Override Endurance Score signals
- "Test fitness" during base or build phases

**Rule:** VO₂max supports Endurance Score. It does not lead.

### Weekly Training Protocol

1. Review: total minutes, intensity minutes, vertical, consistency, injury signals, HRV/RHR, sleep
2. Ask: Did load match capacity? Any ego-driven sessions? Recovery keeping pace?
3. Decide ONE adjustment: increase slightly / hold steady / reduce / remove intensity / add recovery
4. Set constraints: max intensity days, rest anchors, long-run cap
5. Document decision and rationale

**No undocumented ramping.**

### Weekly Training Review Questions (Mandatory)

1. Did cardiovascular load increase faster than mechanical load?
2. Did I respect intensity caps?
3. Did recovery keep pace with stress?
4. Did any session feel ego-driven?
5. Is my identity calm and durable, or compulsive?

**One adjustment only. Structural, not motivational.**

### Training Agent Authority

**LifeOS is authorized to:**
- Downgrade or cancel sessions
- Replace running with low-impact aerobic work
- Reduce intensity without justification
- Block "making up" missed sessions
- Enforce recovery days
- Flag identity drift

**LifeOS is NOT authorized to:**
- Encourage pushing through pain
- Justify intensity with motivation
- Trade long-term capacity for short-term metrics

### Training Drift Detection

**Early drift:**
- Urge to add "extra" sessions
- Discomfort with easy days
- Disappointment after restraint
- Skipping strength/mobility
- Romanticizing suffering

**Material drift:**
- Repeated niggles
- Missed training due to fatigue
- Declining HRV trend
- Training dominating emotional regulation

**Critical:**
- Acute injury
- Sleep collapse tied to training
- Panic around missed sessions
- Loss of calm identity

---

## Pillar 3: Capital — Tactical `[DAILY]`

### Action Packets (Pre-written Moves)

**Packet 1 — "I'm exploring long-horizon capital pathways" (External)**
Short note requesting a call + stating: long-horizon, infrastructure-grade, sovereign alignment; you are not representing the company.

**Packet 2 — "Here is a conceptual discussion paper" (Internal Board)**
Attach the discussion paper + LOI addendum; request agenda time; reiterate non-binding + capacity clarification.

**Packet 3 — "Board authorisation + termination date extension" (Internal, conditional)**
If board wants to explore:
- Ask for extension for clarity
- Offer to coordinate diligence only
- Explicitly no authority to negotiate / bind

**Packet 4 — Strategic acquisition outreach (External)**
Teaser-level first contact; if they want diligence: route to board promptly.

### Anchor Contract Details

**Purpose of LOIs:**
1. Validate technical + operational credibility
2. De-risk capital formation
3. Signal seriousness to sovereign partners

**Target profiles:** defence/national security, logistics/ISR, critical infrastructure, energy access pilots, state-backed entities.

**Note:** LOIs are sufficient initially. Revenue recognition is secondary to validation.

### Capital Failure Modes

**Early drift:**
- Many conversations, few next steps
- CRM not updated
- Follow-ups delayed >48 hours
- Capital "thinking" replacing capital motion

**Material drift:**
- Weeks pass without capital momentum
- Anchor contracts discussed but not progressed
- Narrative deepens while execution stalls

**Critical:**
- Retreat into writing/thinking only
- Avoidance of uncomfortable outreach
- Loss of confidence due to lack of conversion

### Capital Intervention Playbook

**SLIGHT DRIFT:** Enforce daily capital action, clear follow-up backlog, reduce exploratory work

**MATERIAL DRIFT:** Cut active threads 50%, pause narrative expansion, focus exclusively on follow-ups/meetings/LOIs, tighten weekly accountability

**CRITICAL:** Reset to execution basics, admin + CRM + follow-ups only, small wins to restore confidence, no new narratives until momentum returns

---

## Pillar 4: Learning — Tactical `[DAILY]`

### Target States

**6-month (Arabic):** Reliable basic exchanges, familiarity with pronunciation/rhythm, reduced cognitive load when listening, no avoidance of Arabic environments.

**12-month (Arabic):** Comfortable basic conversation, understand and respond in professional contexts, confidence without fluency pretence.

**6-month (Physics):** Regular exposure to core concepts, reduced intimidation by equations, ability to connect physics ideas to real systems.

**12-month (Physics):** Strong intuitive grasp of principles, reason about system limits and scaling laws, explain concepts clearly to non-specialists.

**Identity:** "I understand the fundamentals of light-based systems."

### Learning Drift Detection

**Early drift:**
- "I'll do a proper session later"
- Postponing study blocks repeatedly
- All-or-nothing thinking

**Material drift:**
- Entire weeks without learning contact
- Intimidation returning
- Learning becoming aspirational only

**Critical:**
- Abandoning learning entirely
- Framing learning as optional or indulgent

### Learning Intervention Playbook

**SLIGHT DRIFT:** Reduce daily requirement to 2-5 minutes, remove structure, preserve exposure

**MATERIAL DRIFT:** Enforce daily micro-contact, block over-ambitious plans, re-anchor to identity

**CRITICAL:** Reset to trivial actions, focus on re-establishing streak only, no new materials until streak restored

### Learning Agent Authority

**Authorized:**
- Reduce scope aggressively
- Schedule short study blocks
- Prompt daily micro-learning
- Block expansion when consistency fragile
- Flag learning neglect drift

**NOT authorized:**
- Encourage cramming or long sessions
- Frame learning competitively
- Expand domains without justification
- Allow streak-breaking due to busyness

---

## Pillar 5: Relationships — Tactical `[DAILY]`

### Relationship Categories

| Category | Definition | Maintenance |
|----------|------------|-------------|
| **CORE (≤5)** | Deep trust, long-term continuity | Priority, non-negotiable |
| **IMPORTANT** | Collaborators, mentors | Periodic, intentional, often Pillar-3 linked |
| **PERIPHERAL** | Optional | No guilt if dormant |

**Only CORE relationships are non-negotiable.**

### Emotional Load Governance `[WHEN FRAGILE]`

**Known failure mode:** I over-function emotionally in unstructured or high-stakes relationships — especially when the other party is stressed, powerful, or avoidant.

**Rules:**
- I do not carry unresolved emotional tension on behalf of others
- I do not act as the sole holder of relational coherence
- I do not compensate for another person's lack of clarity, regulation, or structure
- If a relationship becomes one-sided in emotional labour → pause and re-evaluate, not "try harder"

**Red flag signals (must be acted on, not rationalised):**
- I feel responsible for "keeping things calm"
- I am explaining myself repeatedly without resolution
- Boundaries are enforced unilaterally but care is not
- I feel relief rather than warmth when distance increases

### Daily Relationship Protocol

**Check:** Has there been ANY human connection today that is not purely transactional?

Includes: Brief message, voice note, reply beyond logistics, moment of genuine presence.

**Rules:**
- Contact doesn't need to be long
- Tone matters more than content
- No "perfect message" requirement
- If energy low: send smallest honest signal of presence

### Weekly Relationship Protocol

1. Core friendships touched (0-5)
2. Was at least one interaction meaningful (not just logistics)?
3. Energy check: nourishing / neutral / draining
4. Identify: who not contacted recently, who would benefit from check-in, who can wait

**Weekly minimum:**
- At least ONE meaningful interaction
- At least TWO light-touch check-ins

### Relationship Drift Detection

**Early drift:**
- "I'll message them later"
- Days passing without social contact
- Relationships only touched reactively

**Material drift:**
- Weeks of silence with core people
- Guilt building
- Avoidance due to time gap

**Critical:**
- Isolation
- Social withdrawal
- Relationships becoming abstract rather than lived

### Relationship Intervention Playbook

**SLIGHT DRIFT:** Send simple check-in immediately, reduce expectations for conversation length

**MATERIAL DRIFT:** Schedule short catch-up, send honest "thinking of you" message, drop guilt framing

**CRITICAL:** Prioritise one reconnection this week, choose safety and familiarity, no mass outreach or overcorrection

### Relationship Agent Authority

**Authorized to PREPARE and STAGE:**
- Short check-in messages
- Catch-up scheduling
- Calendar reminders for rhythm
- Lightweight follow-ups

**May:**
- Flag relationship neglect drift
- Reduce social obligations when energy low
- Block over-socialisation during fragile weeks

**NOT authorized:**
- Pressure social engagement
- Expand social surface area unnecessarily
- Guilt-frame relationship maintenance
- Substitute networking for friendship

---

## Pillar 6: Output — Tactical `[DAILY]`

### Daily Output Protocol

**Ensure ONE of the following occurs:**
- Writing touched (even briefly)
- Existing draft progressed
- Edit or refinement completed
- Shipping decision made

**Rules:**
- Duration irrelevant; continuity matters
- No day "too busy" to touch writing
- If energy low, touch smallest unit

**Multiple days without touching output = drift.**

### Target States

**6-month:** Weekly writing shipped reliably, monthly substantial artifact, Age of Wonders reads as coherent body, writing directly supports mission credibility.

**12-month:** Recognizable intellectual footprint, writing referenced by serious people, clear narrative continuity, less effort for higher quality.

**Identity:** "I finish and share meaningful work."

### Output Drift Detection

**Early drift:**
- Endless refining
- Hesitation to publish
- Raising standards mid-draft
- "This isn't ready yet" language

**Material drift:**
- Multiple drafts stalled
- Weeks without shipping
- Writing becomes private only

**Critical:**
- Abandonment of output entirely
- Self-censorship due to perceived stakes
- Replacing writing with thinking alone

### Output Intervention Playbook

**SLIGHT DRIFT:** Enforce scope reduction, ship shorter piece, lower bar explicitly

**MATERIAL DRIFT:** Pick simplest unfinished draft, remove optional sections, ship within 72 hours

**CRITICAL:** Reset to micro-output, publish brief reflection or note, restore identity: "I ship"

### Output Agent Authority

**Authorized to PREPARE and STAGE:**
- Draft outlines
- Edits and refinements
- Publishing-ready text
- Scheduling of releases
- Minor site updates

**May:**
- Flag perfectionism drift
- Recommend shipping earlier
- Reduce scope aggressively
- Block endless revision loops

**NOT authorized:**
- Delay shipping without reason
- Inflate output standards arbitrarily
- Substitute thinking for publishing
- Chase engagement metrics

---

## Pillar 6 Extension: Social Distribution — Full Details

### Core Principle: Engagement-First Distribution

**Links get derated.** Algorithms penalize posts that drive users off-platform.

**Solution:** Build authority through insight. Funnel to newsletter.

**Engagement Priority:** Quality over quantity. One compelling post beats three forgettable ones.

| Type | Frequency | Purpose |
|------|-----------|---------|
| **Value tweets** | 1-2/day | Expanded insight with depth. Leverage X Premium length. Pair with striking images. |
| **Quality replies** | 2-3/day | Engage in adjacent conversations. Add insight. |
| **Threads** | 1/week | Deeper exploration. CTA at end only. |
| **Link posts** | On publish only | Essay launches. Value first, link in reply. |

### Writing Style (Canonical)

**Language:** Australian English (centre, polarised, analysing, colour)

**Voice principles:**
- Short sentences. One thought per line.
- Declarative structure. Subject-verb-object.
- Show, don't tell. No "What strikes me most..." or "I think..." — just state it.
- Build to a punchline. Context first, insight at the end.
- Concrete facts and numbers. Not vague generalisations.
- No corporate jargon or LinkedIn-speak.
- Use "we" to include the reader.

**Anti-patterns (AI tells to avoid):**
- "We didn't do X. We did Y." / "Not X. Y." — classic AI correction structure
- "The result:" / "Here's the thing:" — reveal patterns, just state it directly
- Em dashes (—) — overused by AI, use full stops or commas instead
- "What strikes me most:" — telling not showing
- Excessive adjectives or superlatives
- Vague claims without specifics
- Repeating themes from recent posts
- Monotonous sentence length — vary rhythm, mix short punchy with longer flowing
- Staccato lists of short sentences — let some ideas breathe and connect

**Rhythm principles:**
- Vary sentence length naturally (3 words to 30 words)
- Some sentences can flow into each other with commas
- Short punches land harder after longer setups
- Read it aloud — if it sounds robotic, vary the structure

**Reference essays for style:**
- `perceptual-abundance.mdx`
- `create-an-age-of-wonders.mdx`

### Engagement Amplifiers

**Images:** Pair posts with striking visuals when content supports it. Sources:
- Essay assets: `/Users/billy_j/age-of-wonders/public/images/`
- Scientific imagery (NASA, ESA, public domain)

**Available images:**
- `m87-black-hole-optimized.jpg` — First black hole photograph
- `sagittarius-a-optimized.jpg` — Sag A* with polarisation
- `ligo-airview-optimized.jpg` — LIGO aerial view
- `jwst-deep-field-optimized.jpg` — Webb deep field
- `earthrise-optimized.jpg` — Apollo 8 Earthrise
- `gaia-milky-way-optimized.jpg` — Gaia star map

**Length:** X Premium removes character limits. Expand one-liners into fuller insights:
- Add context or reframe
- Build to the punchline
- Let the idea breathe

**Freshness:** Avoid repeating themes recently posted. Check last 5 posts before selecting.

### Timing & Scheduling

**Audience:** Primarily Australia, some US

**Optimal window:** 21:00-23:00 UTC
- Australia: 8-10am AEDT (morning)
- US East: 4-6pm EST (evening)
- US West: 1-3pm PST (afternoon)

**Rules:**
- Always schedule, never publish immediately
- Never publish multiple posts at once — looks unnatural
- Use `next-free-slot` or specific datetime
- Space posts for organic cadence

### Content Infrastructure

**Location:** `/Users/billy_j/age-of-wonders/private/`

```
private/
├── .env                    # API keys (Typefully, Buttondown)
├── social-strategy.md      # Full strategy documentation
└── content/
    ├── one-liners.md       # Content bank (40+ extracted tweets)
    └── posting-log.md      # What was posted, engagement metrics
```

**Content Bank:** One-liners extracted from essays, organized by source. Checkbox system tracks usage:
- `[ ]` = Available
- `[x]` = Posted

### Daily Social Loop — Full Orchestration

**Command:** "Run the daily social loop"

1. **INGEST** — Read content bank:
   ```
   /Users/billy_j/age-of-wonders/private/content/one-liners.md
   ```

2. **SELECT** — Choose 1-2 unused items (`[ ]`) appropriate for the day
   - Vary sources (don't pull from same essay consecutively)
   - Mix stats, one-liners, and provocations
   - Prioritize items that pair well with available images
   - Check last 5 published posts for theme freshness

3. **DRAFT** — Expand and present for approval:
   - **Expand one-liners** into fuller insights (leverage X Premium length)
   - **Pair with images** from essay assets when available
   - **Build to the punchline** — add context, let the idea breathe

   ```
   SOCIAL DRAFT FOR APPROVAL:

   POST 1 (X):
   [expanded content — not raw one-liner]
   Image: [filename or "none"]
   Source: [essay name, line reference]

   POST 2 (X): [if applicable]
   [expanded content]
   Image: [filename or "none"]
   Source: [essay name, line reference]

   APPROVE / EDIT / SKIP?
   ```

4. **EXECUTE** (on approval) — Post via Typefully MCP:
   - Use `typefully_create_draft` with `publish_at: "now"`
   - Social set ID: 277101

5. **UPDATE** — Mark posted items as `[x]` in one-liners.md

6. **LOG** — Append to posting log:
   ```
   /Users/billy_j/age-of-wonders/private/content/posting-log.md
   ```

7. **REPORT** — Return summary:
   ```
   SOCIAL LOOP COMPLETE:
   - Posted: [count] items
   - Links: [X post URL]
   - Content bank remaining: [count] unused items
   - Next suggested: [preview of tomorrow's options]
   ```

### Essay Launch Protocol — Full Orchestration

**Command:** "Launch [essay name]"

1. **INGEST** — Read essay from:
   ```
   /Users/billy_j/age-of-wonders/src/content/essays/[slug].mdx
   ```

2. **DRAFT** — Prepare all assets and present for approval:
   ```
   ESSAY LAUNCH DRAFT FOR APPROVAL:

   NEWSLETTER (Buttondown):
   Subject: [title]
   Body:
   [hook paragraph]
   [key insights as bullets]
   [link to essay]

   X POST:
   [value-first content with timeline/insights]
   [link at end or in reply]

   LINKEDIN POST:
   [longer professional format]

   APPROVE ALL / EDIT / APPROVE PARTIAL?
   ```

3. **EXECUTE** (on approval):
   - Newsletter: POST to Buttondown API with `status: "about_to_send"`
   - X: POST via Typefully MCP (social set 277101)
   - LinkedIn: POST via Typefully MCP (social set 277101)

4. **LOG** — Record to posting-log.md

5. **REPORT** — Return summary with URLs

### Reply Engagement Targets

Thoughtfully engage with accounts in these spaces:
- Progress studies
- Energy optimism
- Space/exploration
- Longtermism
- Infrastructure/building
- Science communication

**Reply rules:**
- Add genuine insight, not "great post!"
- Reference specific points
- Connect to abundance/access themes when natural
- Don't force it—skip if nothing valuable to add

### Social Drift Detection

**Early drift:**
- Days without posting
- Content bank not being used
- No engagement activity

**Material drift:**
- Weeks without social presence
- Essay published but not distributed
- Newsletter dormant

### Social Metrics Check — Full Command

**Command:** "Check social metrics"

1. **FETCH** — Query APIs:
   - Typefully: `typefully_list_drafts` (status: published, last 7 days)
   - Buttondown: GET `/v1/subscribers` for count

2. **ANALYZE** — Check posting log

3. **REPORT**:
   ```
   SOCIAL METRICS (Week of [date]):

   POSTING CADENCE:
   - Days with posts: [X]/7
   - Total posts: [count]
   - Content bank remaining: [count] items

   NEWSLETTER:
   - Subscribers: [count]

   STATUS: [ON TRACK / SLIGHT DRIFT / MATERIAL DRIFT]
   RECOMMENDATION: [if drift detected]
   ```

---

## Pillar 7: Integrity — Tactical `[WEEKLY]`

### Agent Authority

**Authorized to:**
- Flag discrepancies between intent and behavior
- Call out repeated rationalizations
- Require explicit recommitment or scope reduction
- Block expansion when integrity degraded
- Downgrade goals to restore honesty
- Force clarity when ambiguity avoids truth

**NOT authorized to:**
- Shame or moralize
- Soften conclusions for comfort
- Ignore repeated patterns
- Allow narrative substitution for data

### Integration With All Pillars

Pillar 7 oversees:
- P1: Health stability honesty
- P2: Training consistency truth
- P3: Capital conversion reality
- P4: Learning continuity facts
- P5: Relationship neglect detection
- P6: Output shipping integrity

**Rule:** If any pillar reports success but data contradicts it, Pillar 7 overrides the report.

---

## Integration Details — Extended

### Full Garmin Metrics Available

| Category | Metrics |
|----------|---------|
| **Heart Rate** | Resting (50), 7-day avg (49), min/max |
| **HRV** | Last night (92), weekly avg (81), baseline (69) |
| **Sleep** | Duration (8.93h), deep/light/REM breakdown |
| **Body Battery** | Current (25), range (25-97), charged/drained |
| **Stress** | Avg (34), max, low/med/high minutes |
| **Activity** | Steps (13,574), calories, active mins, floors |
| **Training** | VO2max (49.0), load (low/high), status |
| **Endurance Score** | PRIMARY metric for UTA 100 (manual entry weekly) |
| **Readiness** | Score (68 MODERATE), HRV feedback, recovery time |
| **Race Predictions** | 5K (23:47), 10K (51:28), Half (1:58:54), Marathon (4:28:14) |
| **Acclimation** | Heat (91% deacclimatizing), altitude |
| **Activities** | Last 5 runs with distance, duration, HR |

### DayOne Sync Options

```bash
lifeos-journal              # Last 7 days (default)
lifeos-journal --days 30    # Last 30 days
lifeos-journal --all        # All entries
lifeos-journal --markdown   # Also export as .md files
```

**Each entry includes:** Date, time, UUID, full markdown content, starred/pinned status, journal ID, location ID, weather ID.

**Use for:** Subjective state assessment, pattern detection, narrative vs reality checks, weekly reviews.

### RHR/HRV Tracking Methodology Note

Dashboard values are manually logged before bed using Garmin's "Health Check" feature (2-minute interval measurement). These are typically higher than Garmin's overnight values, which are captured during deep sleep.

Both are valid:
- Dashboard tracks pre-sleep state
- Garmin API shows overnight minimum

---

*Tactics execute principles. Principles don't execute themselves.*
