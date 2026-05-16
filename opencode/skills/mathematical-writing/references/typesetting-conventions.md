# Typesetting Conventions

Markdown and LaTeX formatting rules for mathematical documents: document structure, math
environments, tables, figures, and cross-references.

* * *

## Document Structure

### YAML Header

Include a YAML header with document metadata and LaTeX packages:

```yaml
---
title: "Derivatives Problem Set"
author: "Mathematics Department"
date: "2025-06-20"
header-includes:
  - "% Delimiter macros for consistent spacing"
  - "\newcommand{\qty}[1]{\left( #1 \right)}"
  - "\newcommand{\bqty}[1]{\left[ #1 \right]}"
  - "\newcommand{\Bqty}[1]{\left\{ #1 \right\}}"
  - "\newcommand{\abs}[1]{\left| #1 \right|}"
  - "\newcommand{\eval}[1]{\left. #1 \right|}"
  - "\newcommand{\continuedline}{\quad\quad\quad}"
  - "% Left/Right delimiter macros"
  - "\newcommand{\lqty}[1]{\left( #1 \right.}"
  - "\newcommand{\rqty}[1]{\left. #1 \right)}"
  - "\newcommand{\lbqty}[1]{\left[ #1 \right.]}"
  - "\newcommand{\rbqty}[1]{\left. #1 \right]}"
  - "\newcommand{\lBqty}[1]{\left\{ #1 \right.}"
  - "\newcommand{\rBqty}[1]{\left. #1 \right\}}"
---
```

### Section Headers

- Use ATX-style headers with `#` for sections
- Use title case for section headers
- Include a blank line before and after headers

```markdown
# Problem Set 1: Derivatives

## Section 1: Polynomial Functions
```

* * *

## Mathematical Notation

### Inline Math

- Use `$...$` for inline math
- Use proper spacing around operators
- Use `\,` for thin spaces in math mode when needed

**Example:**
```markdown
Find the derivative of $f(x) = x^2 + 3x + 2$.
```

### Display Math

- Use `$$...$$` for displayed equations
- Number important equations using `\tag{n}`
- Align equations at the equals sign when appropriate

**Example:**
```markdown
$$\begin{aligned}
f(x) &= (x+1)^2 \\
     &= x^2 + 2x + 1
\end{aligned}$$
```

### Equation Numbering and Referencing

Number important equations and reference them:

```markdown
$$\label{eq:derivative}
f'(x) = \lim_{h\to 0} \frac{f(x+h) - f(x)}{h}
$$

Equation \eqref{eq:derivative} shows the limit definition of the derivative.
```

* * *

## Problem Formatting

### Problem Statements

- Use clear, concise problem statements
- Include all necessary information
- Use consistent numbering

```markdown
### Problem 1
Find the derivative of $f(x) = \sqrt{x^2 + 1}$ using the limit definition.

### Problem 2
Evaluate the following limit:
$$\lim_{x\to 0} \frac{\sin(3x)}{x}$$
```

### Solutions

- Show all steps clearly
- Use aligned environments for multi-step solutions
- Include brief explanations for non-obvious steps

```markdown
### Solution
We use the limit definition of the derivative:

$$\begin{aligned}
f'(x) &= \lim_{h\to 0} \frac{\sqrt{(x+h)^2 + 1} - \sqrt{x^2 + 1}}{h} \\
     &= \lim_{h\to 0} \frac{\sqrt{x^2 + 2xh + h^2 + 1} - \sqrt{x^2 + 1}}{h} \\
     &\quad\quad\text{(Multiply by the conjugate)} \\
     &= \lim_{h\to 0} \frac{(x^2 + 2xh + h^2 + 1) - (x^2 + 1)}{h(\sqrt{x^2 + 2xh + h^2 + 1} + \sqrt{x^2 + 1})} \\
     &= \lim_{h\to 0} \frac{2xh + h^2}{h(\sqrt{x^2 + 2xh + h^2 + 1} + \sqrt{x^2 + 1})} \\
     &= \lim_{h\to 0} \frac{2x + h}{\sqrt{x^2 + 2xh + h^2 + 1} + \sqrt{x^2 + 1}} \\
     &= \frac{2x}{2\sqrt{x^2 + 1}} \\
     &= \frac{x}{\sqrt{x^2 + 1}}
\end{aligned}$$
```

* * *

## Tables and Figures

### Tables

- Use pipe tables for simple tables
- Align columns with colons
- Use LaTeX math in tables when needed

```markdown
| Function      | Derivative      |
|---------------|-----------------|
| $x^n$         | $nx^{n-1}$      |
| $e^x$         | $e^x$           |
| $\ln x$       | $\frac{1}{x}$   |
| $\sin x$      | $\cos x$        |
| $\cos x$      | $-\sin x$       |
```

### Figures

- Use descriptive captions
- Reference figures in the text
- Use vector graphics (PDF, SVG) for diagrams

```markdown
![Graph of $f(x) = x^2$](graph.pdf)
*Figure 1: Graph of the function $f(x) = x^2$.*
```

* * *

## Cross-References

### Internal Links

- Use Markdown-style links for internal references
- Use descriptive link text

```markdown
See [Problem 1](#problem-1) for an example of polynomial differentiation.
```

* * *

## Best Practices

### Consistency

- Be consistent with notation throughout the document
- Use the same style for similar elements
- Maintain consistent spacing

### Readability

- Break long derivations into multiple steps
- Use comments to explain complex steps
- Use whitespace to separate logical sections

### Version Control

- Use meaningful commit messages
- Keep lines under 80 characters
- Use descriptive file names

* * *

## Common Pitfalls

### Math Mode

- **DO NOT** use text mode inside math mode
- **DO NOT** forget to escape special characters
- **DO NOT** mix text and math mode without proper spacing

### Spacing

- Use proper spacing around operators
- Use `\,` for thin spaces in math mode
- Use `\quad` or `\qquad` for larger spaces

### Alignment

- Align equations at the equals sign
- Use `&` for alignment points
- Use `\\` for line breaks in aligned environments

* * *

## Alignment Examples

### Multi-line Derivation

```markdown
$$\begin{aligned}
A &= B + C \\
  &= D + E \quad \text{[By Lemma 3]} \\
  &= F
\end{aligned}$$
```

### Cases Environment

```markdown
$$f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x & \text{if } x < 0
\end{cases}$$
```

### Matrix

```markdown
$$\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}$$
```

* * *

## Line Length and Wrapping

- Keep source lines under 80 characters where possible
- Break long equations at natural points (before `=`, `+`)
- Use `\continuedline` or `\quad` for visual indentation on continuation lines

* * *

## Typesetting Checklist

Before finalizing a document:

- [ ] YAML header includes all required macros
- [ ] Inline math uses `$...$`, display math uses `$$...$$`
- [ ] Important equations are numbered with `\tag{n}`
- [ ] Multi-step derivations use `aligned` environment
- [ ] Tables use pipe syntax with aligned columns
- [ ] Figures have descriptive captions and are referenced in text
- [ ] Internal cross-references use Markdown links
- [ ] Equation references use `\label` / `\eqref`
- [ ] No text mode inside math mode
- [ ] Proper spacing around all operators
- [ ] Source lines under 80 characters
- [ ] Consistent notation throughout
