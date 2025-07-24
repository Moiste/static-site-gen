# Static Site Generator

A custom static site generator built entirely with Python’s standard library.

This project takes Markdown files and converts them into fully static HTML pages using a custom parsing engine, HTML node tree, and a lightweight templating system. The final output is deployed and viewable as a static site.

**Live Demo:** [moiste.github.io/static-site-gen](https://moiste.github.io/static-site-gen/)

---

## Overview

This site generator processes `.md` files with support for:

- Headings (`#`, `##`, etc.)
- Paragraphs and line breaks
- Blockquotes (`>`)
- Ordered (`1.`) and unordered (`-`) lists
- Code blocks (```)
- Inline formatting:
  - `**bold**`
  - `_italic_`
  - `` `code` ``
  - `[links](url)`
  - `![images](url)`

It uses a custom-built HTML node tree system (like `LeafNode` and `ParentNode`) to structure content semantically and render HTML directly from Markdown input.

---

## Key Concepts

- **Custom Markdown Parser**  
  Splits content into blocks and inline text using Python `re` and delimiter logic.

- **HTML Node Tree**  
  Abstract classes like `TextNode`, `LeafNode`, and `ParentNode` represent parsed content and generate corresponding HTML.

- **Templating Engine**  
  Replaces `{{ Title }}` and `{{ Content }}` in a base HTML template to wrap generated content.

- **Recursive File Handling**  
  Processes entire directories of Markdown content and mirrors structure into an output `public/` folder.

---

## Example

### Markdown Input

```markdown
# Hello World

Welcome to my static site generator.

This is **bold**, _italic_, and `code`.

> A blockquote

- Item 1
- Item 2

1. First
2. Second

![Alt text](image.png)
```

### Generated HTML
```<h1>Hello World</h1>
<p>Welcome to my static site generator.</p>
<p>This is <b>bold</b>, <i>italic</i>, and <code>code</code>.</p>
<blockquote>A blockquote</blockquote>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
<ol>
  <li>First</li>
  <li>Second</li>
</ol>
<img src="image.png" alt="Alt text">
```
