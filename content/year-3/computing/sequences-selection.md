---
year: 3
subject: computing
topic: Sequences and Selection
slug: sequences-selection
key_concepts: [algorithms, sequences, selection, debugging]
age_range: "7-8"
animation: ../../animations/year-3/computing/sequences-selection.html
---

# Sequences and Selection — Year 3 Computing

## What We're Learning
You are going to learn how computers follow instructions. You will discover that a **sequence** is a set of steps in order, and **selection** lets a program choose what to do next. You will also practise **debugging** — finding and fixing mistakes.

## Key Words
| Word | What it means |
|---|---|
| Algorithm | A set of step-by-step instructions to solve a problem. |
| Sequence | Instructions that run one after another, in order. |
| Selection | A decision point — the program checks a condition and chooses what to do. |
| Condition | A question that has a yes/no (true/false) answer. |
| Debug | Finding and fixing errors (bugs) in a program. |
| Input | Information that goes into a program (e.g. a button press). |
| Output | Information that comes out (e.g. text on screen, a sound). |

## Let's Explore

### Sequences

A sequence runs steps **in order**, like a recipe:

```
1. Get a bowl
2. Pour in cereal
3. Add milk
4. Eat!
```

If you swap steps 2 and 3, you get milk then cereal on top — wrong order!

### Selection (If… Then… Else)

Sometimes a program needs to **make a decision**:

```
IF it is raining THEN
    take an umbrella
ELSE
    wear sunglasses
```

The program checks a **condition** (is it raining?) and chooses a path.

### More Examples

```
IF score >= 10 THEN
    display "Well done!"
ELSE
    display "Try again!"
```

```
IF password = "abc123" THEN
    open the door
ELSE
    show "Access denied"
```

### Debugging

Bugs are mistakes in code. A debugger:
1. **Reads** the code carefully
2. **Predicts** what should happen
3. **Tests** the code
4. **Finds** where it goes wrong
5. **Fixes** the bug

**Example bug:**

```
1. Pick up pen
2. Write name
3. Open book      ← Bug! Should be before writing
4. Close book
```

Fix: Move step 3 to before step 2.

## Try It Yourself

1. Put these in the correct sequence: "Brush teeth → Wake up → Get dressed → Eat breakfast"
2. Write a selection statement: IF (something) THEN (do this) ELSE (do that) — choose your own scenario.
3. Find the bug: "1. Put on shoes. 2. Put on socks. 3. Tie laces."
4. What is the condition in: "IF temperature > 30 THEN turn on fan"?
5. Is "Open the door" a sequence, selection, or a single instruction?

<details>
<summary>Check your answers</summary>

1. Wake up → Get dressed → Eat breakfast → Brush teeth
2. Any valid if-then-else — e.g. "IF homework is done THEN play outside ELSE finish homework"
3. Socks should come before shoes. Correct: 1. Put on socks. 2. Put on shoes. 3. Tie laces.
4. temperature > 30
5. A single instruction (one step).

</details>

## Did You Know? 💻
The first computer "bug" was a real moth! In 1947 a moth got stuck inside a computer at Harvard University. The engineers taped it into their log book and wrote "first actual case of bug being found."

## Learning Checklist
- [ ] I can explain what a sequence is
- [ ] I can write a selection statement (IF… THEN… ELSE)
- [ ] I can identify and fix a bug in a sequence
- [ ] I can describe what input and output mean
---
year: 3
subject: computing
topic: Sequences and Selection
slug: sequences-selection
key_concepts: [If/then logic, branching programs, Scratch basics]
age_range: "7-8"
animation: ../../animations/year-3/computing/sequences-selection.html
---

# Sequences and Selection — Year 3 Computing

## What We're Learning
You are going to learn how computers follow instructions in order — this is called a **sequence**. You will also learn how computers make decisions using **selection**: choosing what to do next based on a yes-or-no question. You will explore these ideas using Scratch.

## Key Computing Words
| Word | What it means |
|---|---|
| Sequence | A set of instructions carried out one after another, in order |
| Selection | When a computer checks a condition and decides what to do next |
| Condition | A question the computer asks that has a yes or no answer |
| If/then | A rule that says "if this is true, then do this" |
| Branch | A different path the program can follow depending on the answer |
| Algorithm | A step-by-step set of instructions to solve a problem |
| Input | Information you give to the computer, like pressing a key |
| Debug | Finding and fixing mistakes in a program |

## The Big Idea
Think about getting dressed in the morning. You follow a sequence — first you put on your socks, then your shoes. The order matters! If you put your shoes on first, your socks cannot go on.

Computers follow sequences too. They carry out each instruction in the exact order you give them.

But sometimes, the next step depends on a question. For example: **Is it raining?** If yes, take an umbrella. If no, leave the umbrella at home. This is called **selection** — the computer selects which path to follow.

In a program, selection looks like this:

```
IF it is raining THEN
    take umbrella
ELSE
    leave umbrella at home
```

### Sequences — Order Matters

A **sequence** is a set of instructions in a fixed order.

**Example — making a sandwich:**
1. Get two slices of bread
2. Spread butter on both slices
3. Add cheese in the middle
4. Put the slices together

If you swap step 4 and step 2, the result is very different!

### Selection — Making Decisions

Sometimes a program needs to choose between two paths. It asks a **condition** (a yes/no question) and follows one path for YES and a different path for NO.

```
  START
    ↓
  Is it sunny?
   /       \
  YES       NO
   ↓         ↓
  Wear      Take an
  sunhat    umbrella
   ↓         ↓
  Go outside
```

### Selection in Scratch

In Scratch, you use the orange **"if … then"** block or the **"if … then … else"** block. You place a diamond-shaped condition block inside it:

- `if <key space pressed?> then` → move 10 steps
- `if <touching edge?> then` → turn around

### Combining Sequence and Selection

Real programs mix both ideas. A character in a game might:
1. Move forward (sequence)
2. Check — am I touching the edge? (selection)
   - YES → bounce back
   - NO → keep moving
3. Repeat from step 1

### Debugging

When your program does not behave as you expect, you **debug** it:
1. Read each instruction in order.
2. Check the sequence — is the order correct?
3. Check each condition — does it ask the right question?
4. Fix the mistake and test again.

## Unplugged Activity
**Human Robot Game**

Work with a partner. One person is the "robot" and the other is the "programmer".

1. The programmer writes instructions on cards — one instruction per card (e.g. "take two steps forward").
2. The robot follows the cards in exact order (sequence).
3. Now add a decision card: "IF you reach a wall THEN turn right ELSE keep walking."
4. The robot must check the condition and choose the correct path.

Try programming a route around the classroom using sequences and at least two decision cards.

## On the Computer
**Making a Branching Program in Scratch**

1. Open Scratch on the classroom computer.
2. Choose a sprite — perhaps a cat or a parrot.
3. From **Events**, drag "when green flag clicked" to the scripts area.
4. From **Looks**, add a "say [Hello!] for 2 seconds" block.
5. From **Sensing**, add an "ask [Do you like cats — yes or no?] and wait" block.
6. From **Control**, drag an "if … then … else" block.
7. From **Operators**, put "answer = yes" into the diamond space.
8. Inside the "if" section, add "say [Me too — cats are wonderful!] for 2 seconds".
9. Inside the "else" section, add "say [That is OK — everyone is different!] for 2 seconds".
10. Click the green flag and test with both answers.

## Challenge
Add a second question after the first one. Your program should now have two "if … then … else" blocks one after the other. Can you make the sprite respond differently to three or four answers?

## Stay Safe Online
When you use Scratch, you do not need to share your real name or any personal details. Use a made-up username if your teacher asks you to save your work. Never share your password with anyone except a trusted adult.

## Think Like a Computer Scientist
1. What is the difference between a sequence and selection?
2. Look at this algorithm: "Spread butter. Get bread. Put bread in toaster." What is wrong with the order?
3. What would happen if you changed the condition from "IF it is sunny" to "IF it is windy"?
4. How would you design a program that asks your favourite colour and gives a different fun fact for each answer?

## Learning Checklist
- [ ] I can explain what a sequence is and put instructions in the correct order
- [ ] I can use selection (if/then) to make a program choose between two paths
- [ ] I can explain what a condition is in my own words

## Sources
- UK National Curriculum — Computing, Year 3: design, write and debug programs that accomplish specific goals; use sequence, selection and repetition in programs
- NCCE Teach Computing — Year 3 Unit: Programming — Sequencing and Selection
