---
year: 5
subject: computing
topic: Web Design
slug: web-design-y5
key_concepts: [HTML basics, web pages, content, layout]
age_range: "9-10"
animation: ../../animations/year-5/computing/web-design-y5.html
---

# Web Design — Year 5 Computing

## Big Question
How are web pages made and what is HTML?

## What We're Learning
In this lesson you will learn the basics of **HTML**, how web pages are structured with **tags**, and how **content** and **layout** work together.

## Key Computing Words
| Word | What it means |
|---|---|
| HTML | HyperText Markup Language — the code used to build web pages |
| tag | a code instruction wrapped in angle brackets, e.g. `<h1>` |
| element | an opening tag, content, and closing tag together |
| heading | a title on a web page, written with `<h1>` to `<h6>` |
| paragraph | a block of text, written with `<p>` |
| attribute | extra information inside a tag (e.g. `src` in an image tag) |

## The Computing Explained

### What Is HTML?
HTML is the language that **every web page** is built with. Your browser reads HTML and displays it as text, images, and links.

### Basic Structure
```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Page</title>
  </head>
  <body>
    <h1>Welcome!</h1>
    <p>This is my first web page.</p>
  </body>
</html>
```

### Common Tags
| Tag | What it does |
|---|---|
| `<h1>` to `<h6>` | Headings (h1 = biggest) |
| `<p>` | Paragraph of text |
| `<img>` | Displays an image |
| `<a>` | Creates a link to another page |
| `<ul>` / `<li>` | Bulleted list |
| `<strong>` | Bold text |

### How Tags Work
Every tag has an **opening** and a **closing** tag:
```html
<p>Hello world</p>
```
Some tags are self-closing: `<img src="photo.jpg" />`

### Planning a Web Page
1. Decide on the **purpose** — what is the page about?
2. Plan the **layout** — headings, paragraphs, images.
3. Write the **HTML**.
4. **Test** in a browser.

## Quick Quiz
1. What does HTML stand for? → *HyperText Markup Language*
2. Which tag makes the biggest heading? → *`<h1>`*
3. What does the `<p>` tag do? → *Creates a paragraph of text*
4. What is an attribute? → *Extra information inside a tag*

## Computing in the Real World
Every website you visit is built with HTML. Web developers use HTML alongside CSS (for styling) and JavaScript (for interactivity) to create the sites and apps you use every day.

## Learning Checklist
- [ ] I can explain what HTML is and why it is used
- [ ] I can identify common HTML tags
- [ ] I can plan and describe the structure of a simple web page
