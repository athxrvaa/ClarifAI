# ClarifAI Documentation (static site)

This folder contains a simple static documentation site for the ClarifAI project.

- `index.html` — The documentation homepage describing the project, architecture, how it works, setup, and impacts/benefits.
- `styles.css` — Minimal styling for the doc page.

How to view locally:

1. Open `d:/ClarifAI/docs/index.html` in your browser (double-click or use `File -> Open`).
2. Or serve the folder with Python from the workspace root:

```powershell
python -m http.server 8000
# then open http://localhost:8000/docs/
```

Notes:
- The content is intentionally high-level. If you want expanded API docs, CLI reference or auto-generated docs from code, I can add those next.
