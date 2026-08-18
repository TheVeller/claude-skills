# ASCII hero templates (readme-commit)

Use inside `<div align="center">` wrapped in `<pre>…</pre>` (or a fenced code block that GitHub centers via the div). Keep width ~50–60 columns. Prefer a template over improvising broken art.

## Template A — double box (graphify-remote style)

Best default for product/plugin names.

```text
╔══════════════════════════════════════════════════╗

   YOURASCIIHERE
   (block letters or short wordmark)

  PRODUCT DISPLAY NAME
  tagline bit  ·  tagline bit  ·  tagline bit

╚══════════════════════════════════════════════════╝
```

Example shape (replace letters for the product):

```text
╔══════════════════════════════════════════════════╗

   ██████╗ ██╗   ██╗
  ██╔════╝ ██║   ██║
  ██║  ███╗██║   ██║
  ██║   ██║╚██╗ ██╔╝
  ╚██████╔╝ ╚████╔╝
   ╚═════╝   ╚═══╝

  GRAPHIFY OBSIDIAN VISUALIZER
  Obsidian plugin  ·  Graphify bridge  ·  embed graph.html

╚══════════════════════════════════════════════════╝
```

## Template B — short block wordmark

When the name is short (≤8 letters) and a full box feels heavy:

```text
 ____
|  _ \ __ _  __ _  __ _
| |_) / _` |/ _` |/ _` |
|  __/ (_| | (_| | (_| |
|_|   \__,_|\__, |\__,_|
            |___/
```

Generate letters with a local figlet-style pass if available; otherwise hand-fit Template A.

## Rules

1. Subtitle lines live **inside** the box (Template A), not only under the H1.
2. Do not replace the ASCII hero with a third-party product logo; small logos go in the Compatible-with strip under badges.
3. After the `</pre>`, use `# Title` (H1) + bold one-liner — graphify remote order.
