# Primary School Curriculum Map
> UK National Curriculum — Years 1–6 (Ages 5–11)

This file is the **single source of truth** for the content-generation pipeline. Each agent reads this file to know which subject, year, and topics to generate content and animations for.

---

## How to read this file

Each leaf topic is an **atomic unit** of content generation. The orchestrator iterates every topic entry and dispatches the appropriate subject agent to produce:

1. `content/year-{Y}/{subject}/{topic-slug}.md` — lesson content
2. `animations/year-{Y}/{subject}/{topic-slug}.html` — interactive animation

Topic slugs use kebab-case and match the file names agents must write.

---

## Year 1 — Ages 5–6

### Maths
| Topic | Slug | Key Concepts |
|---|---|---|
| Counting to 100 | `counting-to-100` | Count forwards/backwards, number lines, one-to-one correspondence |
| Addition and Subtraction | `addition-subtraction` | Number bonds to 20, +/- within 20, part-whole model |
| 2D and 3D Shapes | `shapes-2d-3d` | Circle, square, triangle, rectangle, cube, sphere, cylinder |
| Measurement — Length | `measurement-length` | Longer/shorter, taller/shorter, measuring with non-standard units |
| Measurement — Weight | `measurement-weight` | Heavier/lighter, balance scales, grams |
| Ordinal Numbers | `ordinal-numbers` | 1st–10th, position language |

### English
| Topic | Slug | Key Concepts |
|---|---|---|
| Phonics — Phase 3 | `phonics-phase3` | Digraphs (ch, sh, th), vowel digraphs (ai, ee, oa) |
| Phonics — Phase 4 | `phonics-phase4` | Adjacent consonants (CCVC, CVCC words), tricky words |
| Sentence Writing | `sentence-writing` | Capital letters, full stops, finger spaces, conjunctions (and) |
| Rhyme and Poetry | `rhyme-poetry` | Nursery rhymes, rhyming pairs, rhythm clapping |
| Storytelling | `storytelling` | Story structure (beginning, middle, end), characters, setting |

### Science
| Topic | Slug | Key Concepts |
|---|---|---|
| Animals Including Humans | `animals-including-humans` | Body parts, senses, basic needs (food, water, air) |
| Seasonal Changes | `seasonal-changes` | Four seasons, daylight hours, weather patterns |
| Everyday Materials | `everyday-materials` | Wood, plastic, glass, metal, water; properties (hard, soft, rough) |
| Plants | `plants-year1` | Parts of a plant, what plants need to grow |

### History
| Topic | Slug | Key Concepts |
|---|---|---|
| Changes Within Living Memory | `changes-living-memory` | Transport, technology, toys — then and now |
| Significant Historical Events | `significant-historical-events-y1` | Bonfire Night, Great Fire of London — sequencing events |

### Geography
| Topic | Slug | Key Concepts |
|---|---|---|
| Our Local Area | `local-area` | School surroundings, maps, aerial photographs, compass directions |
| Hot and Cold Places | `hot-cold-places` | North/South Pole, equator, Africa, Arctic animals |

### Computing
| Topic | Slug | Key Concepts |
|---|---|---|
| Algorithms and Instructions | `algorithms-instructions` | Ordering steps, giving clear directions, unplugged activities |
| Creating Digital Content | `creating-digital-content-y1` | Drawing with computers, keyboard skills, saving work |

---

## Year 2 — Ages 6–7

### Maths
| Topic | Slug | Key Concepts |
|---|---|---|
| Place Value to 100 | `place-value-100` | Tens and ones, comparing numbers, number lines to 100 |
| Times Tables 2, 5, 10 | `times-tables-2-5-10` | Multiplication as repeated addition, arrays, grouping |
| Fractions — Half and Quarter | `fractions-half-quarter` | ½, ¼ of shapes and quantities, equivalence |
| Measurement — Money | `measurement-money` | Coins and notes, totalling, giving change |
| Statistics — Block Diagrams | `statistics-block-diagrams` | Reading and drawing block graphs, tally charts |

### English
| Topic | Slug | Key Concepts |
|---|---|---|
| Reading Fiction | `reading-fiction-y2` | Inference, character feelings, story language |
| Reading Non-Fiction | `reading-non-fiction-y2` | Contents, headings, glossary, finding information |
| Punctuation | `punctuation-y2` | Exclamation marks, question marks, apostrophes (omission) |
| Grammar — Word Classes | `grammar-word-classes` | Nouns, verbs, adjectives, adverbs |
| Recount Writing | `recount-writing` | First person, time connectives, past tense |

### Science
| Topic | Slug | Key Concepts |
|---|---|---|
| Living Things and Habitats | `living-things-habitats` | Micro-habitats, food chains, classification (living/dead/never lived) |
| Plants — Growth | `plants-growth` | Germination, what affects growth, parts and functions |
| Uses of Everyday Materials | `uses-materials-y2` | Changing shapes (squash, bend, twist, stretch), suitable materials |

### History
| Topic | Slug | Key Concepts |
|---|---|---|
| Great Fire of London | `great-fire-of-london` | 1666, Samuel Pepys, how fire spread, changes after |
| Significant People — Florence Nightingale | `florence-nightingale` | Nursing, Crimean War, improving hospitals |
| Significant People — Neil Armstrong | `neil-armstrong` | Moon landing 1969, space exploration, timeline |

### Geography
| Topic | Slug | Key Concepts |
|---|---|---|
| Continents and Oceans | `continents-oceans` | 7 continents, 5 oceans, world map orientation |
| UK Countries and Capital Cities | `uk-countries-capitals` | England, Scotland, Wales, Northern Ireland |

### Computing
| Topic | Slug | Key Concepts |
|---|---|---|
| Debugging Algorithms | `debugging-algorithms` | Finding and fixing errors in sequences, logical thinking |
| Online Safety | `online-safety-y2` | Personal information, safe websites, kind communication |

---

## Year 3 — Ages 7–8

### Maths
| Topic | Slug | Key Concepts |
|---|---|---|
| Place Value to 1000 | `place-value-1000` | Hundreds, tens, ones; comparing; rounding to nearest 10/100 |
| Multiplication and Division | `multiplication-division-y3` | Times tables 3, 4, 8; formal written methods |
| Fractions | `fractions-y3` | Unit fractions, non-unit fractions, adding/subtracting same denominator |
| Perimeter | `perimeter-y3` | Measuring perimeter of 2D shapes, rectilinear shapes |
| Statistics — Bar Charts | `statistics-bar-charts` | Drawing and reading bar charts, pictograms |

### English
| Topic | Slug | Key Concepts |
|---|---|---|
| Narrative Writing | `narrative-writing-y3` | Story openings, build-up, climax, resolution; show don't tell |
| Poetry — Imagery | `poetry-imagery-y3` | Similes, personification, imagery, performing poems |
| Report Writing | `report-writing-y3` | Formal tone, sub-headings, facts, present tense |
| Conjunctions and Clauses | `conjunctions-clauses` | Subordinating (because, although, when), main/subordinate clause |

### Science
| Topic | Slug | Key Concepts |
|---|---|---|
| Rocks and Fossils | `rocks-fossils` | Types of rock (igneous, sedimentary, metamorphic), fossil formation |
| Light and Shadows | `light-shadows` | Light sources, reflections, shadow formation, sundials |
| Forces and Magnets | `forces-magnets` | Push, pull, friction, magnetic attraction/repulsion |
| Plants — Functions | `plants-functions-y3` | Photosynthesis (intro), plant lifecycle, pollination, seed dispersal |

### History
| Topic | Slug | Key Concepts |
|---|---|---|
| Stone Age to Iron Age | `stone-age-iron-age` | Prehistoric Britain, Stonehenge, tools, farming, Celts |
| Ancient Egypt | `ancient-egypt` | Pharaohs, mummies, hieroglyphics, River Nile, pyramids |

### Geography
| Topic | Slug | Key Concepts |
|---|---|---|
| Volcanoes and Earthquakes | `volcanoes-earthquakes` | Tectonic plates, structure of Earth, famous eruptions |
| Mountains | `mountains-y3` | Highest mountains, mountain ranges, mountain climates |

### Computing
| Topic | Slug | Key Concepts |
|---|---|---|
| Sequences and Selection | `sequences-selection` | If/then logic, branching programs, Scratch basics |
| Data and Information | `data-information-y3` | Collecting data, databases, searching |

---

## Year 4 — Ages 8–9

### Maths
| Topic | Slug | Key Concepts |
|---|---|---|
| Place Value to 10,000 | `place-value-10000` | Thousands; ordering; rounding to nearest 1000 |
| All Times Tables | `times-tables-all` | 6, 7, 9, 11, 12; rapid recall strategies |
| Decimals | `decimals-y4` | Tenths, hundredths; comparing; rounding |
| Area | `area-y4` | Area of rectangles, counting squares |
| Roman Numerals | `roman-numerals` | I, V, X, L, C, D, M — reading years |

### English
| Topic | Slug | Key Concepts |
|---|---|---|
| Playscripts | `playscripts-y4` | Stage directions, character voice, dialogue punctuation |
| Persuasive Writing | `persuasive-writing-y4` | AFOREST, rhetorical questions, opinion vs. fact |
| Fronted Adverbials | `fronted-adverbials` | Comma after fronted adverbial, sentence variety |
| Reading — Inference and Deduction | `reading-inference-y4` | Evidence from text, author intent, vocabulary in context |

### Science
| Topic | Slug | Key Concepts |
|---|---|---|
| Electricity | `electricity-y4` | Simple circuits, conductors/insulators, switches |
| Sound | `sound-y4` | Vibrations, pitch, volume, how sound travels |
| Living Things — Classification | `living-things-classification-y4` | Vertebrates/invertebrates, grouping organisms |
| States of Matter | `states-of-matter` | Solid, liquid, gas; melting, freezing, evaporation, condensation |

### History
| Topic | Slug | Key Concepts |
|---|---|---|
| Ancient Greece | `ancient-greece` | City states, democracy, Olympics, mythology, philosophers |
| Roman Britain | `roman-britain` | Roman invasion, legions, roads, Boudicca, Roman legacy |

### Geography
| Topic | Slug | Key Concepts |
|---|---|---|
| Rivers | `rivers-y4` | River features (source, tributary, mouth), water cycle, famous rivers |
| UK Regions | `uk-regions` | Counties, physical/human features, Ordnance Survey maps |

### Computing
| Topic | Slug | Key Concepts |
|---|---|---|
| Repetition in Programming | `repetition-programming` | Loops (repeat, forever), Scratch animations |
| Creating Media — Animation | `creating-media-animation` | Frame-by-frame animation, flipbooks, GIF concepts |

---

## Year 5 — Ages 9–10

### Maths
| Topic | Slug | Key Concepts |
|---|---|---|
| Fractions, Decimals, Percentages | `fractions-decimals-percentages` | Equivalences, converting, percentage of amounts |
| Geometry — Properties of Shapes | `geometry-properties` | Angles (acute, obtuse, reflex), regular/irregular polygons |
| Statistics — Line Graphs | `statistics-line-graphs` | Reading/drawing line graphs, interpreting data |
| Long Multiplication | `long-multiplication` | 4-digit × 2-digit, grid method, column method |
| Negative Numbers | `negative-numbers` | Number lines, temperature, calculating differences |

### English
| Topic | Slug | Key Concepts |
|---|---|---|
| Biographies | `biographies-y5` | Chronological structure, reported speech, formal language |
| Argument Writing | `argument-writing-y5` | For/against, balanced argument, modal verbs |
| Classic Literature | `classic-literature-y5` | Extracts from Charles Dickens, Roald Dahl — inference, themes |
| Relative Clauses | `relative-clauses` | Who, which, where, when, whose; embedded clauses |

### Science
| Topic | Slug | Key Concepts |
|---|---|---|
| Earth and Space | `earth-space-y5` | Solar system, day/night, seasons, moon phases, gravity |
| Forces | `forces-y5` | Gravity, air resistance, water resistance, levers, pulleys |
| Properties of Materials | `properties-materials-y5` | Thermal/electrical conductivity, solubility, transparency |
| Living Things — Life Cycles | `life-cycles-y5` | Mammals, insects (metamorphosis), amphibians, plants |

### History
| Topic | Slug | Key Concepts |
|---|---|---|
| Ancient Maya | `ancient-maya` | Maya civilisation, calendar, cities, farming, decline |
| Victorian Britain | `victorian-britain` | Industrial Revolution, child labour, inventions, social change |

### Geography
| Topic | Slug | Key Concepts |
|---|---|---|
| Biomes and Climate Zones | `biomes-climate-zones` | Rainforest, desert, tundra, grassland — animals, plants, climate |
| Trade and Globalisation | `trade-globalisation` | Supply chains, fair trade, interdependence |

### Computing
| Topic | Slug | Key Concepts |
|---|---|---|
| Variables in Programming | `variables-programming` | Storing/changing values, score counters, Scratch games |
| Web Design | `web-design-y5` | HTML basics, hyperlinks, images, page structure |

---

## Year 6 — Ages 10–11

### Maths
| Topic | Slug | Key Concepts |
|---|---|---|
| Algebra | `algebra-y6` | Formulae, linear sequences, unknowns, substitution |
| Ratio and Proportion | `ratio-proportion` | Ratio notation, scale factors, percentage problems |
| Geometry — Coordinates | `geometry-coordinates` | Four quadrants, translations, reflections |
| Fractions Division | `fractions-division-y6` | Dividing fractions, mixed numbers |
| SATs Problem Solving | `sats-problem-solving` | Multi-step worded problems, reasoning and proof |

### English
| Topic | Slug | Key Concepts |
|---|---|---|
| SATs Reading Preparation | `sats-reading-prep` | Retrieval, inference, vocabulary, author intent questions |
| Formal and Informal Writing | `formal-informal-writing` | Register, passive voice, subjunctive mood |
| Narrative Writing — Y6 | `narrative-writing-y6` | Atmosphere, tension, varied sentence structures, literary devices |
| Speeches and Debate | `speeches-debate` | Rhetoric, structuring an argument, confident delivery |

### Science
| Topic | Slug | Key Concepts |
|---|---|---|
| Evolution and Inheritance | `evolution-inheritance` | Adaptation, natural selection, fossils as evidence, Darwin |
| Living Things — Classification | `living-things-classification-y6` | Taxonomic groups, classification keys, microorganisms |
| Light | `light-y6` | Reflection, refraction, colour spectrum, lenses |
| Electricity — Circuits | `electricity-circuits-y6` | Voltage, resistance, circuit diagrams, series vs parallel |

### History
| Topic | Slug | Key Concepts |
|---|---|---|
| World War II | `world-war-ii` | Causes, Blitz, evacuation, key figures, turning points, legacy |
| The British Empire | `british-empire` | Colonisation, trade routes, impact on colonised countries, legacy |

### Geography
| Topic | Slug | Key Concepts |
|---|---|---|
| Sustainability | `sustainability-y6` | Climate change, deforestation, renewable energy, global footprint |
| Globalisation | `globalisation-y6` | Migration, cultural exchange, international organisations |

### Computing
| Topic | Slug | Key Concepts |
|---|---|---|
| Binary and Data Representation | `binary-data` | Binary numbers, ASCII, file sizes, compression concepts |
| Networks and Cybersafety | `networks-cybersafety` | How the internet works, passwords, phishing, digital footprint |

---

## Pipeline Configuration

```yaml
# Used by orchestrator.agent.md to drive the generation loop
output_root: ../content
animation_root: ../animations
years: [1, 2, 3, 4, 5, 6]
subjects: [maths, english, science, history, geography, computing]
content_format: markdown
animation_format: html
agent_map:
  maths:     .github/maths-agent.agent.md
  english:   .github/english-agent.agent.md
  science:   .github/science-agent.agent.md
  history:   .github/history-agent.agent.md
  geography: .github/geography-agent.agent.md
  computing: .github/computing-agent.agent.md
animation_agent: .github/animation-generator.agent.md
```
