---
name: deck-local-export
description: >-
  Use when a design tool (for example Futuraria) can't export a finished deck
  to PDF or PPTX and you need shareable files for a call recap.
---
# Export a deck locally when the design tool has no export

1. Render each finished frame at 2x as PNG and check every render for overflow or overlap. Fix and re-render if needed.
2. Build the PDF with real selectable text (HTML per slide printed to PDF), not only images.
3. Build the PPTX with one full-bleed 2x image per slide and the slide text in the speaker notes.
4. Upload both to Drive as private. Share the PPTX only with the external attendees as viewer, without notification. Never use anyone-with-the-link and never publish.
5. When a deck is revised after its link was sent, overwrite the same Drive file so the file id and link stay the same.
6. Keep build scripts and renders in one workspace folder per call so the deck can be rebuilt.
7. Attach the PPTX to the meeting's notes row and embed the Drive file on its page.
