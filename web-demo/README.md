Gemma Web Demo

A minimal mock web UI that mirrors the Android app's quiz screens and uses a fake model response.

Setup

Install dependencies and run dev server:

```bash
cd web-demo
npm install
npm run dev
```

Open the URL printed by Vite (usually http://localhost:5173) and click "Generate Lesson" to preview the UI.

Next steps
- Replace `src/mockModel.js` with real inference calls (Hugging Face API or WebLLM runtime).
- Build production bundle with `npm run build`.
