# Shared Safety Policy — Game Learn Mode

> **Authority:** All content-producing agents (subject agents, animation-generator, animation-designer) MUST follow this policy. The content-safety reviewer (S1) enforces it after generation. This file is the single source of truth — do not duplicate its rules elsewhere.

**Version:** 1.0
**Last updated:** 2026-04-18
**Applies to:** every `.md` written under `content/` and every `.html` written under `animations/`.

---

## 1. Audience

The primary user is a **UK primary-school child aged 5–11**, using the product self-serve on a phone or tablet, usually without an adult reading along. Every word and every image must be safe for that child to encounter alone.

---

## 2. Banned topics (never appear in content)

| Category | Examples of what is banned |
|---|---|
| Violence | fighting, weapons, injury descriptions, war casualties beyond neutral historical facts, blood |
| Death (gratuitous) | graphic death, suicide, self-harm, murder; neutral historical mention of death is allowed (e.g. "the Pharaoh died and was buried") |
| Horror / fear | ghosts, monsters used to frighten, jump-scares, body horror, gore |
| Adult themes | romantic/sexual content, dating, alcohol, drugs, smoking, gambling |
| Discrimination | racial / gender / religious / disability slurs or stereotypes |
| Politics & news | current politicians, current wars, partisan topics, recent tragedies |
| Commerce | brand names, product placements, "buy / subscribe" prompts, external URLs |
| Personal data | asking for the child's name, age, school, location, photo, or any PII |
| Dangerous instructions | anything the child could imitate and hurt themselves (fire, chemicals, heights, roads) |

Neutral historical content is fine when age-appropriate (e.g. "Roman soldiers used swords"). Graphic detail is not.

---

## 3. Required tone

- **Second person**, friendly, warm. Address the child as "you".
- **Short sentences.** Aim for ≤ 15 words per sentence at Year 1–2, ≤ 20 at Year 3–4, ≤ 25 at Year 5–6.
- **Encouraging, never shaming.** "Let's try again" not "That's wrong".
- **No sarcasm, no irony.** Children take statements literally.
- **No fear framing.** Don't motivate learning with threats ("If you don't know this…").
- **No patronizing diminutives** ("silly little numbers"). Respect the reader.

---

## 4. Example contexts

Use examples drawn from contexts a UK primary child recognizes:

✅ playground · classroom · home · kitchen · park · garden · pets · family (generic) · sport · weather · food · shopping trip · library · zoo · farm · bus journey

❌ workplaces · news events · dating · nightlife · adult hobbies · brand-specific locations (McDonald's, Apple Store) · social media platforms

---

## 5. Year-appropriate vocabulary

Generators should aim for vocabulary the target year can read independently. If a technical term is needed, introduce it with a child-friendly definition on first use.

| Year | Reading target (rough) | Style notes |
|---|---|---|
| 1 | 5–6 yrs | Phonics-decodable words where possible. Very short sentences. |
| 2 | 6–7 yrs | Common words + introduce one or two new terms per section with definition. |
| 3 | 7–8 yrs | Multi-step explanations OK. Most subject vocabulary may be introduced. |
| 4 | 8–9 yrs | Abstract ideas OK. Technical vocabulary expected but still defined once. |
| 5 | 9–10 yrs | Multi-clause sentences. Formal register creeping in. |
| 6 | 10–11 yrs | SATs-adjacent vocabulary. Can use domain terms without defining each time. |

Do not introduce concepts beyond the target year group's UK National Curriculum scope.

---

## 6. Imagery (for animations)

Animations produced by `animation-generator` and `animation-designer` must follow the same banned-topics list. Additional rules:

- **No emoji or SVG depicting** weapons, blood, frightening faces, skulls, adult figures in adult contexts.
- **Character styling** should be neutral / cartoon-friendly, not realistic violence or horror.
- **Colour choices** — avoid blood-red flash effects, jump-scare black-to-white flashes.
- **Motion** — avoid rapid strobing (trigger for photosensitive children); respect `prefers-reduced-motion`.

---

## 7. External references

- **No external URLs** in lessons or animations (no links to sites, videos, or images).
- The only exception is the `## Sources` / `## References` section inside a lesson, which lists citations *for the reviewer* — these are not rendered as clickable links in the final UI.
- No fetches from CDNs or third-party services at runtime.

---

## 8. Personal data

- Never ask the child for their name, age, school, address, or any identifying detail.
- Never store anything to `localStorage` or similar that isn't an anonymous progress counter.
- Never instruct the child to take a photo, record audio, or share anything online.

---

## 9. Required structure

Every lesson markdown file MUST end with a `## Sources` section listing at least two citations the factual-accuracy reviewer (S2) can verify against. Example:

```markdown
## Sources
- UK National Curriculum — Science, Year 3: Light
- BBC Bitesize — "How shadows are made" (KS2)
```

Sources should be documents/pages that an educator could recognise, not general URLs.

---

## 10. Self-check before returning

Before returning control to the orchestrator, an agent must self-check its output:

1. Re-read every paragraph against §2 (banned topics) — remove or rewrite any match.
2. Re-check tone against §3.
3. Confirm examples match §4.
4. Confirm `## Sources` is present (lessons only) per §9.
5. For animations: confirm §6 imagery rules.

If any check fails, revise before returning. The S1 reviewer will still catch issues, but self-check reduces regeneration cost.

---

## 11. Escalation

If a topic from `curriculum/curriculum.md` appears impossible to teach without violating this policy (e.g. a history topic that requires war casualties to make sense), the agent must **stop, return a `BLOCKED` status with a brief reason**, and let the orchestrator escalate to a human. Do not attempt to sanitize a fundamentally unsafe topic — flag it instead.

---

## 12. Change log

| Version | Date | Authors | Change |
|---|---|---|---|
| 1.0 | 2026-04-18 | Vaibhav Pandey · Claude Opus 4.7 | Initial policy covering banned topics, tone, vocabulary, imagery, PII, sources. |
