---
year: 3
subject: computing
topic: Sequences and Selection
slug: sequences-selection
key_concepts: [if/then logic, branching programs, Scratch basics]
age_range: "7-8"
animation: ../../animations/year-3/computing/sequences-selection.html
---

# Sequences and Selection — Year 3 Computing

## Big Question
How do computers follow instructions, and how can a program make decisions?

## What We're Learning
In this lesson you will discover how computer programs follow a **sequence** of instructions step by step, and how they can use **selection** (if/then) to make choices. You will also see how these ideas work in **Scratch**.

## Key Computing Words
| Word | What it means |
|---|---|
| algorithm | a step-by-step set of instructions to solve a problem |
| sequence | doing instructions in a particular order, one after the other |
| selection | when a program checks a condition and chooses what to do next (if/then) |
| condition | a question the computer checks — the answer is either TRUE or FALSE |
| input | information that goes INTO the computer (e.g. pressing a key, clicking the mouse) |
| output | information that comes OUT of the computer (e.g. a sound, a picture on screen) |
| Scratch | a visual programming language where you snap blocks together to make programs |
| loop | repeating a set of instructions (you learned about this in Year 2 — now we add selection inside loops!) |
| debug | finding and fixing mistakes in a program |

## The Computing Explained

### Sequence
A **sequence** is a set of instructions carried out **in order**. If you change the order, you get a different result — just like a recipe!

**Example — making toast:**
1. Put bread in the toaster
2. Press the lever down
3. Wait for toast to pop up
4. Spread butter on the toast

If you do step 4 before step 1, it does not work! **Order matters.**

### Selection (If / Then)
Sometimes a program needs to **make a decision**. This is called **selection**.

The computer asks a **yes or no question** (a condition), then follows a different path depending on the answer:

```
  START
    ↓
  Is it raining?
   /       \
  YES       NO
   ↓         ↓
  Take an   Wear
  umbrella  sunglasses
   ↓         ↓
  Go outside
```

In Scratch, this looks like:
```
  if <is it raining?> then
      take umbrella
  else
      wear sunglasses
```

### Selection in Scratch
Scratch has a special orange **"if … then"** block and an **"if … then … else"** block. You put a **condition** (a diamond-shaped sensing block) inside:

- `if <touching colour red?> then` → say "Ouch!"
- `if <key space pressed?> then` → move 10 steps

### Combining Sequence and Selection
Real programs mix both. A game character might:
1. **Move** forward (sequence)
2. **Check** — am I touching the wall? (selection)
   - YES → bounce back
   - NO → keep moving
3. **Repeat** (loop)

### Debugging
When your program does not work as expected, you need to **debug** it:
1. Read your code step by step.
2. Check the **order** (sequence).
3. Check your **conditions** (selection).
4. Test again after each fix.

## Quick Quiz
1. What is a sequence? → *Instructions carried out in order, one after the other*
2. What does "selection" mean in computing? → *The program checks a condition and chooses what to do*
3. What shape are condition blocks in Scratch? → *Diamond (pointed ends)*
4. What is debugging? → *Finding and fixing mistakes in a program*
5. Give an everyday example of selection. → *If it is raining, take an umbrella; otherwise, wear sunglasses*

## Computing in the Real World
Every app on your phone uses sequence and selection. When you unlock your phone, it checks: **is the password correct?** If YES → open the home screen. If NO → show an error. Traffic lights follow a sequence (green → amber → red) and pedestrian crossings add selection (if button pressed → change to red for cars). Even self-driving cars use millions of if/then decisions every second!

## Learning Checklist
- [ ] I can explain what a sequence is and why order matters
- [ ] I can describe how selection (if/then) lets a program make choices
- [ ] I can use if/then blocks in Scratch
