# Game Learn Mode — System Architecture

> How the agent pipeline generates lesson content, converts it to interactive animations, and exposes the learning library to an application.

---

## 1. System Overview

The platform is built around three layers: a **curriculum definition**, an **agent pipeline**, and a **learning library** of static files that any app can serve directly.

```mermaid
flowchart TD
    CM["📄 curriculum/curriculum.md\nSingle source of truth\n96 topics · Years 1–6"]

    subgraph AGENTS["Agent Pipeline"]
        OA["🎯 Orchestrator Agent\norchestrator.agent.md"]

        subgraph SUBJECT["Subject Agents"]
            MA["➗ Maths Agent"]
            EA["📖 English Agent"]
            SA["🔬 Science Agent"]
            HA["🏛️ History Agent"]
            GA["🌍 Geography Agent"]
            CA["💻 Computing Agent"]
        end

        AN["🎨 Animation Generator Agent\nanimation-generator.agent.md"]
    end

    subgraph OUTPUT["Generated Library"]
        CF["content/\nyear-{Y}/{subject}/{slug}.md\nLesson markdown files"]
        AF["animations/\nyear-{Y}/{subject}/{slug}.html\nSelf-contained HTML games"]
        PR["content/PIPELINE_REPORT.md\nRun summary"]
    end

    subgraph APP["Application Layer"]
        WA["Web App / Static Server\nServes HTML animations directly"]
        RI["Reading Interface\nRenders lesson markdown"]
        NAV["Navigation / Index\nBrowse by year & subject"]
    end

    CM -->|"read on startup"| OA
    OA -->|"dispatch per topic"| SUBJECT
    SUBJECT -->|"write lesson file"| CF
    CF -->|"read before generating"| AN
    AN -->|"write game file"| AF
    OA -->|"write after run"| PR
    CF --> RI
    AF --> WA
    CM --> NAV
```

---

## 2. Curriculum Structure

The curriculum markdown is the **only** file agents are allowed to read as their input definition. It encodes every year, subject, topic, slug, and key concepts in one place.

```mermaid
erDiagram
    CURRICULUM ||--o{ YEAR : contains
    YEAR ||--o{ SUBJECT : has
    SUBJECT ||--o{ TOPIC : defines

    CURRICULUM {
        string pipeline_config
        string output_root
        string animation_root
    }
    YEAR {
        int number "1 to 6"
        string age_range "e.g. 5-6"
    }
    SUBJECT {
        string name "maths | english | science | history | geography | computing"
        string agent_file
    }
    TOPIC {
        string title
        string slug "kebab-case file name"
        string key_concepts "comma-separated"
        string content_path "content/year-Y/subject/slug.md"
        string animation_path "animations/year-Y/subject/slug.html"
    }
```

### Topic count by year and subject

```mermaid
xychart-beta
    title "Topics per Year (all subjects)"
    x-axis ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"]
    y-axis "Number of topics" 0 --> 20
    bar [17, 15, 17, 16, 16, 15]
```

---

## 3. Orchestrator Loop

The orchestrator is the entry point for the entire pipeline. It reads the curriculum, builds a task list, and loops through every topic — dispatching a subject agent then an animation agent for each one.

```mermaid
flowchart TD
    START(["`**Start**
    @orchestrator generate all content`"])
    READ["Read curriculum/curriculum.md\nExtract all topics into flat list"]
    TODO["Build TodoWrite task list\nOne entry per topic"]
    LOOP{{"For each topic\nin the list"}}

    CHECK{"content_path\nAND animation_path\nalready exist?"}
    SKIP["Mark todo done\nSkip to next"]

    DISPATCH_S["Dispatch Subject Agent\n— pass year, subject, topic_title,\nslug, key_concepts, output_file"]
    WAIT_S{{"Wait for\nDONE: {content_path}"}  }
    ERR_S["Log error\nMark todo BLOCKED\nContinue to next topic"]

    DISPATCH_A["Dispatch Animation Generator Agent\n— pass content_file, output_file"]
    WAIT_A{{"Wait for\nDONE: {animation_path}"}}
    ERR_A["Log error\nMark todo BLOCKED\nContinue to next topic"]

    DONE["Mark todo done\n✅ Both files written"]

    MORE{"More topics?"}
    REPORT["Write content/PIPELINE_REPORT.md\nTopics processed · Files written\nErrors · File tree"]
    END([End])

    START --> READ --> TODO --> LOOP
    LOOP --> CHECK
    CHECK -->|"yes (no --force)"| SKIP
    CHECK -->|"no"| DISPATCH_S
    DISPATCH_S --> WAIT_S
    WAIT_S -->|"success"| DISPATCH_A
    WAIT_S -->|"error"| ERR_S
    DISPATCH_A --> WAIT_A
    WAIT_A -->|"success"| DONE
    WAIT_A -->|"error"| ERR_A
    DONE --> MORE
    ERR_S --> MORE
    ERR_A --> MORE
    SKIP --> MORE
    MORE -->|"yes"| LOOP
    MORE -->|"no"| REPORT --> END
```

### Scope filtering

The orchestrator accepts optional filters so you can regenerate a subset without touching the full library:

```mermaid
flowchart LR
    ARG["User argument"] --> P{Parse filter}
    P -->|"year=3"| FY["Filter: Year 3 only\n17 topics"]
    P -->|"subject=maths"| FS["Filter: Maths only\nAll years · ~30 topics"]
    P -->|"year=2 subject=science"| FYS["Filter: Y2 Science\n3 topics"]
    P -->|"topic=counting-to-100"| FT["Filter: Single topic\n1 topic"]
    P -->|"--force"| FF["No skip check\nOverwrite existing files"]
    P -->|"(none)"| FA["Full curriculum\n96 topics"]
```

---

## 4. Content Generation Pipeline

Each subject agent receives a task prompt from the orchestrator and writes a single markdown lesson file. Every agent follows the same input/output contract.

```mermaid
sequenceDiagram
    actor OA as Orchestrator Agent
    participant SA as Subject Agent<br/>(e.g. Maths Agent)
    participant FS as File System

    OA->>SA: Dispatch task with context block:<br/>year · subject · topic_title · slug<br/>key_concepts · output_file

    SA->>FS: Read curriculum/curriculum.md<br/>(validate topic exists)

    note over SA: Compose lesson content:<br/>• What We're Learning<br/>• Key Words table<br/>• Worked Examples<br/>• Practice Questions + Answers<br/>• Fun Fact<br/>• Learning Checklist

    SA->>FS: Write content/year-{Y}/{subject}/{slug}.md

    SA-->>OA: DONE: content/year-{Y}/{subject}/{slug}.md
```

### Lesson file anatomy

```mermaid
block-beta
    columns 1
    FM["🗂️ YAML Frontmatter\nyear · subject · topic · slug · key_concepts · age_range · animation path"]
    WL["📝 What We're Learning\n2–3 sentences · direct address · age-appropriate vocabulary"]
    KW["🔑 Key Words Table\nTerm → child-friendly definition"]
    EX["🔢 Let's Explore\nStep-by-step explanation · worked examples · ASCII diagrams"]
    PQ["✏️ Try It Yourself\n5 graded practice questions · collapsible answer key"]
    FF["💡 Fun Fact / Real-World Connection"]
    CL["☑️ Learning Checklist\n3 concrete 'I can...' statements"]
```

### Subject agent specialisations

```mermaid
flowchart LR
    subgraph AGENTS["Subject Agents"]
        MA["➗ Maths\nNumber lines · arrays\ncolumn methods · ASCII art\nUK curriculum terminology"]
        EA["📖 English\nPhonics phases · grammar glossary\nmodel texts · word banks\nwriting frames"]
        SA2["🔬 Science\nInvestigation ideas\nhousehold materials only\nhypothesis → conclusion Y5+"]
        HA2["🏛️ History\nNarrative storytelling\ntimeline ASCII art\nkey people table\nCE/BCE dating Y3+"]
        GA2["🌍 Geography\nReal place names\nphysical + human geography\nmap activity every lesson"]
        CA2["💻 Computing\nUnplugged first\nno installs\nScratch web · Notepad\npseudocode only"]
    end
```

---

## 5. Animation Generation Pipeline

After the content file is written, the orchestrator dispatches the animation generator agent. This agent reads the content, picks the best interaction archetype for the subject and year, and writes a fully self-contained HTML file.

```mermaid
sequenceDiagram
    actor OA as Orchestrator Agent
    participant AG as Animation Generator Agent
    participant FS as File System
    participant BR as Browser (child)

    OA->>AG: Dispatch with: year · subject · topic_slug<br/>content_file · output_file

    AG->>FS: Read content_file (the lesson markdown)

    note over AG: Extract from content:<br/>• key_concepts from frontmatter<br/>• vocabulary from Key Words table<br/>• questions / examples for quiz data<br/>• core learning objective

    note over AG: Select archetype by subject × year:<br/>e.g. Y1 Maths → click-and-count grid<br/>Y3 Science → shadow puppet canvas<br/>Y4 Computing → circuit builder drag-drop

    note over AG: Compose single HTML file:<br/>• Inline <style> — CSS variables, keyframes<br/>• Interactive DOM / Canvas element<br/>• Embedded question data (from content)<br/>• Vanilla JS — no libraries<br/>• Score tracker · feedback · accessibility

    AG->>FS: Write animations/year-{Y}/{subject}/{slug}.html

    AG-->>OA: DONE: animations/year-{Y}/{subject}/{slug}.html

    BR->>FS: Open .html file directly in browser
    note over BR: Zero server needed —<br/>file:// protocol works fine
```

### Animation archetype selection

```mermaid
flowchart TD
    READ["Read content file\nExtract: year · subject · topic type"]

    READ --> MATHS{"Subject\n= Maths?"}
    READ --> ENG{"Subject\n= English?"}
    READ --> SCI{"Subject\n= Science?"}
    READ --> HIST{"Subject\n= History?"}
    READ --> GEO{"Subject\n= Geography?"}
    READ --> COMP{"Subject\n= Computing?"}

    MATHS -->|"Y1–2 counting"| A1["🔢 Click-and-count grid\n100-square with 4 game modes"]
    MATHS -->|"Y1–2 shapes"| A2["🔷 Shape sorter\ndrag shapes to outlines"]
    MATHS -->|"Y3–4 multiplication"| A3["✖️ Array builder\nclick rows/cols, see product"]
    MATHS -->|"Y3–4 fractions"| A4["🍕 Pizza slicer\nclick to divide animated shape"]
    MATHS -->|"Y4–5 place value"| A5["🃏 Number machine\ndrag digit cards to columns"]
    MATHS -->|"Y5–6 statistics"| A6["📊 Bar chart builder\nclick +/- to change bars"]

    ENG -->|"Y1–2 phonics"| B1["🔤 Word builder\nclick phoneme tiles to blend"]
    ENG -->|"Y3–4 grammar"| B2["🗂️ Word class sorter\ndrag to noun/verb/adjective buckets"]
    ENG -->|"Y3–4 punctuation"| B3["❓ Punctuation placer\nclick correct mark for sentence"]

    SCI -->|"Y1–2 body/plants"| C1["🏷️ Label the diagram\ndrag labels to parts"]
    SCI -->|"Y3–4 light"| C2["🔦 Shadow puppet simulator\ncanvas — drag object, shadow updates live"]
    SCI -->|"Y4 electricity"| C3["⚡ Circuit builder\ndrag components, bulb lights when complete"]
    SCI -->|"Y5 solar system"| C4["🪐 Orbit simulator\nplanets animate, click for facts"]

    HIST -->|"All years"| D1["⏳ Timeline drag\ndrag events to correct position"]
    HIST -->|"Y3–6"| D2["🃏 True/False quiz\nflipping cards with explanations"]

    GEO -->|"Y1–2 maps"| E1["🗺️ Map maker\nclick to place landmarks on grid"]
    GEO -->|"Y2–3 continents"| E2["🌍 Continent click quiz\nworld outline, click regions"]
    GEO -->|"Y5–6 climate"| E3["🌡️ Climate zone explorer\nclick zone, scene animates"]

    COMP -->|"Y1–2 algorithms"| F1["🤖 Robot programmer\narrow buttons, grid path"]
    COMP -->|"Y5–6 binary"| F2["💡 Binary decoder\ntoggle bits, decimal updates live"]
```

### HTML file anatomy (every animation)

```mermaid
block-beta
    columns 1
    HD["📋 HTML Head\n<meta charset> · viewport · <title>"]
    CSS["🎨 Inline <style>\n:root CSS variables (colours, radius)\nReset · Layout · Component styles\n@keyframes (bounce, shake, fadeInUp)\nprefers-reduced-motion guard"]
    HDR["🏷️ Header\nYear tag · Topic title · One-line instruction"]
    SCORE["📊 Score / Progress bar\nLive score · Round counter · Streak (where applicable)"]
    STAGE["🎮 Interactive Stage\nCanvas or DOM interaction area\nDrag-drop / click / slider controls"]
    FB["💬 Feedback Region\naria-live · Correct/wrong messages\nExplanation on wrong answer"]
    DATA["📦 Embedded Data\nconst QUESTIONS = [...]\nExtracted from the lesson content file"]
    JS["⚙️ Vanilla JavaScript\nState management · Event listeners\nFisher-Yates shuffle · requestAnimationFrame\nNo eval · No innerHTML with dynamic data\nNo external requests"]
```

---

## 6. File Naming and Path Conventions

Every file in the system is named by a consistent pattern derived from the curriculum slug.

```mermaid
flowchart LR
    SLUG["topic slug\ne.g. counting-to-100"]

    SLUG -->|"content agent writes"| CP["content/year-1/maths/\ncounting-to-100.md"]
    SLUG -->|"animation agent writes"| AP["animations/year-1/maths/\ncounting-to-100.html"]

    CP -->|"frontmatter links to"| AP
    AP -->|"back-link in header"| CP
```

### Directory layout

```
game-learn-mode/
│
├── curriculum/
│   └── curriculum.md              ← source of truth (read-only at runtime)
│
├── .github/
│   └── agents/                    ← GitHub Copilot agent definitions
│       ├── orchestrator.agent.md      ← entry point
│       ├── maths-agent.agent.md
│       ├── english-agent.agent.md
│       ├── science-agent.agent.md
│       ├── history-agent.agent.md
│       ├── geography-agent.agent.md
│       ├── computing-agent.agent.md
│       ├── animation-generator.agent.md
│       └── animation-designer.agent.md
│
├── content/                       ← generated lesson markdown
│   ├── PIPELINE_REPORT.md
│   └── year-{1..6}/
│       └── {subject}/
│           └── {slug}.md
│
├── animations/                    ← generated HTML games
│   └── year-{1..6}/
│       └── {subject}/
│           └── {slug}.html
│
└── doc/
    └── architecture.md            ← this file
```

---

## 7. Exposing Content to an Application

The generated library is **entirely static**. No build step, no server-side rendering, no database. An application consumes it in one of three ways:

```mermaid
flowchart TD
    LIB["📚 Generated Library\ncontent/ + animations/"]

    LIB --> M1
    LIB --> M2
    LIB --> M3

    subgraph M1["Mode 1 — Static File Server"]
        S1["Any static host\n(Nginx · Apache · GitHub Pages\nNetlify · Vercel · local file://)"]
        S1A["Browser opens\nanimations/year-1/maths/counting-to-100.html\ndirectly — zero server logic"]
    end

    subgraph M2["Mode 2 — Embedded in a Framework App"]
        S2["Next.js / Astro / SvelteKit / plain HTML"]
        S2A["Copy content/ and animations/\ninto the framework's public/ or static/ dir"]
        S2B["App reads curriculum.md\nto build navigation index"]
        S2C["Lesson page renders\ncontent markdown via MDX/marked"]
        S2D["Animation loads inside\n<iframe src=animations/.../slug.html>"]
        S2 --> S2A --> S2B
        S2B --> S2C
        S2B --> S2D
    end

    subgraph M3["Mode 3 — Claude Code Extension / Local Dev"]
        S3["Open any .html file\nin browser or VSCode Live Preview"]
        S3A["No server required\nfile:// protocol works for all animations"]
    end
```

### Recommended integration pattern (Framework App)

```mermaid
sequenceDiagram
    actor Child as 👦 Child (browser)
    participant App as Web App
    participant CM as curriculum.md
    participant CF as content/*.md
    participant AF as animations/*.html

    Child->>App: Visit /learn/year-1/maths

    App->>CM: Read curriculum.md\nFind all Y1 Maths topics
    CM-->>App: [{title, slug, key_concepts}, ...]

    App-->>Child: Render topic index page\n(list of topics with icons)

    Child->>App: Click "Counting to 100"

    App->>CF: Read content/year-1/maths/counting-to-100.md
    CF-->>App: Lesson markdown + frontmatter

    App-->>Child: Render lesson page:\n— Explanation · Key Words · Examples\n— "Play the game!" button

    Child->>App: Click "Play the game!"

    App-->>Child: Load animations/year-1/maths/counting-to-100.html\n(in <iframe> or new tab)

    note over Child: Child plays the interactive game\nNo server calls · All logic in the HTML file
```

### iframe embedding pattern

```html
<!-- In your app's lesson page template -->
<iframe
  src="/animations/year-1/maths/counting-to-100.html"
  title="Counting to 100 interactive game — Year 1 Maths"
  width="100%"
  style="border:none; border-radius:16px; aspect-ratio:4/3;"
  loading="lazy"
  sandbox="allow-scripts"
></iframe>
```

> **Security note:** The `sandbox="allow-scripts"` attribute is sufficient because all animation files are fully self-contained — they make no external network requests, use no `localStorage`, and contain no user-generated content.

---

## 8. End-to-End Data Flow Summary

```mermaid
flowchart LR
    NC["📝 National Curriculum\nUK KS1 + KS2"] -->|"manually encoded into"| CM

    CM["curriculum/\ncurriculum.md"]
    CM -->|"read by"| OA

    subgraph OA["🎯 Orchestrator\n(loops 96 topics)"]
        direction TB
        LOOP1["Dispatch subject agent"] --> LOOP2["Receive DONE: content path"]
        LOOP2 --> LOOP3["Dispatch animation agent"]
        LOOP3 --> LOOP4["Receive DONE: animation path"]
    end

    OA -->|"writes"| CF["content/\nyear-Y/subject/slug.md\nLesson markdown"]

    CF -->|"read by"| AG["🎨 Animation\nGenerator Agent"]
    AG -->|"writes"| AF["animations/\nyear-Y/subject/slug.html\nVanilla HTML game"]

    CF -->|"served as"| RI["📖 Reading interface\n(markdown rendered)"]
    AF -->|"served as"| GI["🎮 Game interface\n(HTML opened directly)"]

    RI -->|"child reads"| CHILD["👦 Child learns"]
    GI -->|"child plays"| CHILD
```

---

## 9. Agent Responsibilities Summary

```mermaid
mindmap
  root((game-learn-mode))
    Curriculum
      curriculum.md
        96 topics
        Years 1–6
        6 subjects
        Slugs + key concepts
    Agents
      Orchestrator
        Reads curriculum
        Drives the loop
        Idempotent skip logic
        Error recovery
        Pipeline report
      Subject Agents
        Maths
        English
        Science
        History
        Geography
        Computing
      Animation Generator
        Reads content file
        Picks archetype
        Writes HTML game
        Zero dependencies
    Output
      content/
        Lesson markdown
        YAML frontmatter
        Practice questions
      animations/
        Self-contained HTML
        Canvas / DOM games
        Score tracking
        Accessibility
    App Integration
      Static file server
      iframe embedding
      Framework app
      Navigation from curriculum.md
```

---

## 10. Security and Dependency Policy

All generated files are subject to these hard constraints — enforced in every agent's system prompt:

| Rule | Reason |
|---|---|
| No external `<script src>` or `<link href>` | No CDN dependency risk, works offline, no supply chain exposure |
| No `fetch` / `XMLHttpRequest` in animations | Games run in `sandbox="allow-scripts"` iframes; no data leaves the page |
| No `eval()` or `new Function()` | Prevents code injection vectors |
| `textContent` only for dynamic text (never `innerHTML`) | Prevents XSS even if data were somehow user-influenced |
| No `localStorage` / `sessionStorage` | Children share devices; no cross-session data leakage |
| No npm packages, no build tools | Zero dependency surface; any file is readable and auditable as-is |
| Investigation materials: household items only | Science experiments are safe for unsupervised classroom use |
| `sandbox="allow-scripts"` iframe attribute | Host app gets an extra defence layer when embedding animations |
