**Findings**

- High: Several lesson and game surfaces are not mobile-safe yet. The lesson renderer outputs full-width tables with no horizontal-scroll wrapper in [app/styles.css](/c:/VP/GH/game-learn-mode/app/styles.css:386), while lessons like [mountains-y3.md](/c:/VP/GH/game-learn-mode/content/year-3/geography/mountains-y3.md:19) and [narrative-writing-y3.md](/c:/VP/GH/game-learn-mode/content/year-3/english/narrative-writing-y3.md:55) rely on multi-column tables. The same pattern shows up in games with fixed drawing areas, for example [perimeter-y3.html](/c:/VP/GH/game-learn-mode/animations/year-3/maths/perimeter-y3.html:18) at lines 18-23 and 51, and [statistics-bar-charts.html](/c:/VP/GH/game-learn-mode/animations/year-3/maths/statistics-bar-charts.html:20) at lines 20-27. On a phone these will load, but they will be cramped, overflow, or force tiny labels.

- High: The touch targets and text sizing are too small for a child-first product. The shell uses `.72rem` to `.95rem` text for labels and supporting copy in [app/styles.css](/c:/VP/GH/game-learn-mode/app/styles.css:138) and [app/styles.css](/c:/VP/GH/game-learn-mode/app/styles.css:121), and the games repeat the same pattern, for example [mountains-y3.html](/c:/VP/GH/game-learn-mode/animations/year-3/geography/mountains-y3.html:12) and [statistics-bar-charts.html](/c:/VP/GH/game-learn-mode/animations/year-3/maths/statistics-bar-charts.html:23). The plus/minus buttons in the chart builder are only `28x28` in [statistics-bar-charts.html](/c:/VP/GH/game-learn-mode/animations/year-3/maths/statistics-bar-charts.html:26). That is below a comfortable touch target on phones and too fiddly for younger children.

- Medium: Several interactions are built from clickable `div`s instead of real controls, which hurts keyboard/switch access and generally makes the UI less robust for children. Examples: mountain zones in [mountains-y3.html](/c:/VP/GH/game-learn-mode/animations/year-3/geography/mountains-y3.html:65) with click handlers at line 105, word tiles in [narrative-writing-y3.html](/c:/VP/GH/game-learn-mode/animations/year-3/english/narrative-writing-y3.html:102), and phrase/bucket sorting in [poetry-imagery-y3.html](/c:/VP/GH/game-learn-mode/animations/year-3/english/poetry-imagery-y3.html:60) and line 104. These work with a mouse/touch, but they do not behave like proper buttons.

- Medium: The navigation is still desktop-biased on small screens. Topic titles and concepts are forcibly truncated with ellipsis in [app/styles.css](/c:/VP/GH/game-learn-mode/app/styles.css:330), so a child on a phone may not see enough text to know what they are opening. The only width breakpoint also hard-codes the home grid to three columns in [app/styles.css](/c:/VP/GH/game-learn-mode/app/styles.css:479), which makes the year cards narrow on small phones instead of simply stacking to two columns.

- Medium: The Year 3 lesson writing is still more “content sheet” than “child-led lesson”. For example, [mountains-y3.md](/c:/VP/GH/game-learn-mode/content/year-3/geography/mountains-y3.md:16) goes straight into long definitions and dense factual blocks, and [narrative-writing-y3.md](/c:/VP/GH/game-learn-mode/content/year-3/english/narrative-writing-y3.md:26) uses longer explanations and comparison tables before giving the child something short to do. If the goal is a child using this independently on phone/tablet/desktop, the content needs shorter chunks, more guided prompts, and more “try/check/play” loops.

**Assumptions**

- This review is based on static code inspection only. I did not run browser/device tests.
- If the product is meant for teacher- or parent-guided use, the content density is less serious. If it is meant to be self-serve for children, it is a clear gap.

**Recommended Direction**

- Use [counting-to-100.html](/c:/VP/GH/game-learn-mode/animations/year-1/maths/counting-to-100.html:58) and [light-shadows.html](/c:/VP/GH/game-learn-mode/animations/year-3/science/light-shadows.html:42) as the template: responsive containers, keyboard/touch support, clear feedback, and alternative controls.
- Set a child-first baseline: body text around `16px+`, tap targets `44px+`, fewer tiny uppercase labels, and simpler high-contrast cards.
- Make every lesson/game responsive by default: wrap tables, scale canvases from container size, add phone and tablet breakpoints, and avoid truncating topic names.
- Rewrite Year 3 lesson pages into shorter cards: `Learn`, `Try`, `Play`, `Check`, with plain-language prompts before definitions.

If you want, I can turn this into a concrete patch next and start with a mobile-first pass on the shell plus one animation page.