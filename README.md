# Personal AI Agent

A self-hosted, always-on AI agent that works on tasks while I'm away from the keyboard.
Think of it as my own small version of Grok Bot's "cloud computer": I drop a job into a
queue (eventually by texting it from my phone), the agent works through it using the
Anthropic API, and the results are waiting when I come back.

## Status
Version 1 (2026-10-31): folder task queue, read-and-draft only, with a free dry-run mode.

## Goals
- Run an agent on my Mac mini that can work on tasks while I'm offline
- Text it a task from my phone ("get started on this for the morning")
- Keep it safe: its own folder, narrow permissions, my approval before anything leaves the machine
- Learn each piece as I build it, and document the learning in Notes/

## Planned architecture
- Host: Mac mini (left on, sleep disabled). A cloud server stays an option if I outgrow it.
- A Python program that watches a task queue (a folder, or an email label) and sends each job
  through the Anthropic API with a limited set of tools.
- Results go to an output folder and/or email.
- Start read-and-draft only. Widen permissions one tool at a time.

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdir -p queue && echo "Plan my study week" > queue/plan.txt
python3 agent.py --dry-run     # free test run; drop --dry-run once .env has the key
```
Drafts land in `output/`. See `Notes/2026-10-31-first-agent-version.md` for details.

## Folder layout
- `Notes/`  Dated notes on decisions, concepts learned, and what broke and how I fixed it
- `README.md`  This file
- `agent.py`  The agent: reads tasks from `queue/`, writes drafts to `output/`
- `tests/`  Unit tests (`python3 -m unittest`)
- `queue/`, `output/`  Tasks and drafts (git-ignored, created on first run)
- `claude-project-instructions.md`  Custom instructions for the matching Claude Project
- `.env.example`  Template for `.env` (copy it, add the real API key; `.env` is git-ignored)
- `.gitignore`  Keeps `.env`, Python caches, and macOS files out of Git

## Costs (approximate)
- Mac mini: $0 extra (already owned)
- Anthropic API: a few dollars a month, billed separately from the Claude Pro plan.
  Set a monthly spending cap in the API console.
- Cloud server (only if needed): about $6 to $24 a month depending on size
