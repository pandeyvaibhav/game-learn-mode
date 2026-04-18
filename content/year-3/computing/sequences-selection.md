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
You are going to learn how computers follow instructions in order — this is called a **sequence**. You will also learn how computers make decisions using **selection**, which means choosing what to do next based on a yes-or-no question. You will see how these ideas work in Scratch.

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
