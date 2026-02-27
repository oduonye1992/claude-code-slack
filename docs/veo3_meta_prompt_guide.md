# Veo 3.1 Meta Prompt Guide — Aurie UGC

This document defines the prompt architecture for generating UGC-style video content with Google
Veo 3.1 for Aurie's social media channels.

---

## Technical Specs

| Property | Value |
|---|---|
| Aspect ratio | 9:16 (vertical, mobile-first) |
| Duration | 15–30 seconds |
| Resolution | 1080 × 1920 minimum |
| Style | UGC — authentic, unpolished, handheld feel |
| Platform targets | TikTok, Instagram Reels, YouTube Shorts |

---

## Prompt Architecture

A complete Veo 3.1 prompt has six components. All are required.

### 1. Scene Description

The core visual instruction. Write in present tense, as if describing what the camera sees right now.

**Structure:**
```
[Subject] [action] in [setting]. [Camera movement]. [Lighting]. [Secondary detail].
```

**Example:**
```
A young woman in her mid-twenties sits cross-legged on a worn sofa, phone in hand, exhaling slowly.
Handheld camera drifts gently closer. Late afternoon light filters through gauze curtains.
A half-drunk cup of tea sits on the side table.
```

**Rules:**
- Be specific — describe textures, colours, time of day
- No logos, no text overlays (add separately)
- Include at least one "authentic imperfection" (crumpled pillow, slightly wrinkled shirt)

### 2. Subject Direction

Describe the person(s) in the video — demographics, emotion, physicality.

**Structure:**
```
[Age range], [gender presentation], [ethnicity or physical trait], [emotional state], [small action].
```

**Diversity note:** Rotate through Aurie's three personas — see `knowledge/audience/personas.md`.
Content should reflect real diversity: different ages, skin tones, body types, environments.

**Example:**
```
Late twenties, South Asian woman, hair loosely tied, visibly tired but finding calm, gently tapping
her chest with one hand.
```

### 3. Audio Direction

Veo 3.1 can generate native audio. Specify both music and dialogue/voiceover.

**Structure:**
```
Background: [music mood and tempo]. Voiceover: [tone, pacing, sample line]. [Ambient sound].
```

**Aurie audio palette:**
- Music: lo-fi acoustic, soft piano, ambient nature sounds — never aggressive or fast
- Voiceover: warm, slightly imperfect (not polished ad voice), first-person preferred
- Ambient: city rain, café hum, morning birds — grounds the video in real life

**Example:**
```
Background: soft lo-fi piano, 70 BPM. Voiceover (warm, conversational): "I didn't know what was
wrong, I just knew something was." Ambient: faint traffic, then silence.
```

### 4. Text Overlays

On-screen text appears as captions or hook overlays. Define timing and style.

**Structure:**
```
0:00–0:03 — [Hook text], [font style: clean sans-serif], [colour: white or soft purple].
0:08–0:12 — [Supporting claim or stat].
0:25–0:30 — [CTA text + app name].
```

**Hook formulas** — see `knowledge/content/hooks.md` for the full library. Top performers:
- `POV: you finally asked for help`
- `Nobody talks about what anxiety actually feels like`
- `What if I told you 5 minutes a day could change everything`

### 5. Style and Visual Identity

Reference `knowledge/brand/visual-identity.md` for the full palette. Summary:

| Element | Guidance |
|---|---|
| Colour palette | Soft purples (#7B68EE, #9B89F5), warm neutrals, natural greens |
| Lighting | Warm, golden-hour or soft overcast — never harsh studio light |
| Colour grade | Slightly desaturated, filmic — not vivid or hyper-real |
| Locations | Homes, parks, coffee shops, commutes — never clinical |
| Props | Everyday objects: phones, mugs, journals, headphones |

### 6. Call to Action

Every video ends with a CTA. Aurie's standard CTAs:

```
"Download Aurie — your pocket mental health companion. Link in bio."
"Try Aurie free. 3-minute daily check-ins. No judgment."
"Aurie: talk to someone who gets it, anytime."
```

---

## Complete Prompt Template

```
SCENE: [Scene description — 2–3 sentences]

SUBJECT: [Subject direction — 1–2 sentences]

AUDIO:
  Background: [music mood and tempo]
  Voiceover: [tone and sample line]
  Ambient: [ambient sound]

TEXT OVERLAYS:
  0:00–0:03 — [Hook]
  0:08–0:12 — [Supporting point]
  0:25–0:30 — [CTA]

STYLE:
  Colour grade: [description]
  Lighting: [description]
  Camera: [handheld / stabilised / slow zoom]

DURATION: [15 | 20 | 30] seconds
ASPECT: 9:16
```

---

## UGC Style Guide for Aurie

### What makes Aurie UGC work

1. **Authenticity over polish** — a slightly shaky camera is better than a tripod. Real imperfection
   signals trust.
2. **First-person narrative** — the video speaks from the user's perspective, not a brand's.
3. **The moment before the solution** — show the struggle, then the relief. Never skip the struggle.
4. **Diversity is non-negotiable** — alternate personas across content calendar. See personas.md.
5. **Subtlety over claims** — Aurie doesn't cure anything. It helps. Show the helping.

### What to avoid

- Studio lighting or professional video aesthetic
- Generic stock-footage feel (perfect hair, perfect backdrop)
- Medical claims (see `knowledge/clinical/compliance.md`)
- Showing crisis content — never depict self-harm, acute panic attacks, or suicidal ideation
- Minimising struggle ("just breathe!" energy)
- Any content that implies Aurie replaces therapy

### Trend integration

When a trend drives the prompt, the trend must be:
1. **Relevant** — directly maps to anxiety, burnout, loneliness, mental wellness
2. **Safe** — passes the compliance check
3. **Authentic** — the video would feel natural to Aurie's audience, not forced

---

## Examples

### Example 1 — "Quiet Quitting" trend

```
SCENE: A woman in her early thirties sits at a home desk, laptop open, visibly unfocused. She
closes the lid gently and opens a phone app. Handheld camera, slight motion. Late evening,
warm desk lamp.

SUBJECT: Early thirties, Black woman, natural hair, work-tired but quietly deciding, slight exhale.

AUDIO:
  Background: soft ambient lo-fi, 65 BPM
  Voiceover (relaxed, first-person): "I stopped pretending I was fine. That was the first step."
  Ambient: keyboard clatter fading to silence

TEXT OVERLAYS:
  0:00–0:03 — "POV: you stop performing okay"
  0:10–0:14 — "Burnout is real. So is recovery."
  0:26–0:30 — "Aurie — talk to someone who gets it"

STYLE:
  Colour grade: warm, slightly desaturated
  Lighting: single warm desk lamp, ambient window glow
  Camera: slow drift closer

DURATION: 30 seconds
ASPECT: 9:16
```

### Example 2 — "Sunday Scaries" trend

```
SCENE: A man in his early thirties lies on a couch Sunday evening, scrolling his phone then
setting it face-down. He stares at the ceiling. Camera is wide, then slowly tightens. Living
room, blue-hour light.

SUBJECT: Early thirties, Latino man, in casual clothes, anxious stillness, one hand over chest.

AUDIO:
  Background: soft piano, reverb, 72 BPM
  Voiceover (quiet, honest): "Sunday used to mean dread. Now I have a routine that helps."
  Ambient: distant traffic, apartment sounds

TEXT OVERLAYS:
  0:00–0:03 — "Nobody talks about Sunday anxiety"
  0:09–0:13 — "5 minutes before Monday changes everything"
  0:26–0:30 — "Download Aurie — free 3-min check-in"

STYLE:
  Colour grade: cool blue tones warming to amber by end
  Lighting: window light fading, floor lamp on
  Camera: wide establishing, slow push-in

DURATION: 30 seconds
ASPECT: 9:16
```
