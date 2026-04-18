# Content Changes Manifest
> Edit this file to describe what you want to add, update, or remove.
> Then run the **Content Editor** agent — it reads this file and applies every pending change.
> Completed changes are marked `status: done` automatically.

---

## How to use

Each change is a fenced block with a type header. The Content Editor agent processes every block where `status: pending`.

### Change types

| Type | What it does |
|---|---|
| `ADD_TOPIC` | Adds a new topic to `curriculum.md` and `curriculum.json`, then generates content + animation |
| `ADD_SECTION` | Appends a new section to an existing lesson markdown file |
| `UPDATE_SECTION` | Replaces the content of a named section in an existing lesson |
| `REMOVE_SECTION` | Deletes a named section from an existing lesson |
| `REMOVE_TOPIC` | Removes a topic from `curriculum.md`, `curriculum.json`, and deletes its content + animation files |
| `REGENERATE` | Force-regenerates content and/or animation for a specific topic |
| `UPDATE_ANIMATION` | Regenerates only the animation for a topic (content unchanged) |

---

## Pending Changes

<!-- Add your changes below this line. Copy a template from the examples section. -->

### Example — not active (status: example)

```change
type: ADD_SECTION
status: example
year: 3
subject: maths
slug: place-value-1000
section_title: Real World Connection
after_section: Did You Know?
content: |
  ## Real World Connection
  Place value to 1000 is used every day — the price of a laptop,
  the distance between two cities, or the number of books in a library.
  Can you think of three things at home that have a number over 100?
```

```change
type: UPDATE_SECTION
status: example
year: 3
subject: science
slug: rocks-fossils
section_title: Try It Yourself
content: |
  ## Try It Yourself
  1. Find 3 stones outside. Are they rough or smooth? Light or dark?
  2. Which type of rock do you think each one might be?
  3. Draw each stone and label its properties.
  4. Ask a grown-up to help you search "rock types for kids" to check your answers.
  5. Could any of them contain a fossil? Why / why not?
```

```change
type: ADD_TOPIC
status: example
year: 3
subject: maths
topic_title: Mental Maths Strategies
slug: mental-maths-strategies
key_concepts: doubling, halving, near doubles, bridging through 10, compensating
after_slug: statistics-bar-charts
```

```change
type: REMOVE_TOPIC
status: example
year: 3
subject: computing
slug: data-information-y3
reason: Covered sufficiently within sequences-selection topic
```

```change
type: REGENERATE
status: example
year: 3
subject: history
slug: ancient-egypt
regenerate: both
reason: Add more detail on daily life section and improve the animation quiz questions
```

---

## Completed Changes

<!-- The Content Editor agent moves done items here automatically -->
