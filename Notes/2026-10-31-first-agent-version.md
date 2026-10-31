# First Version of the Agent (2026-10-31)

## What I built
`agent.py` is a task queue in a folder. I drop a `.txt` or `.md` file into `queue/`, run
`python3 agent.py`, and for each task it asks Claude for a draft, saves the draft in `output/`,
and moves the task to `queue/done/`.

## How to run it
1. First time only: `python3 -m venv .venv` makes a private Python install for this project
   (a **virtual environment**), and `source .venv/bin/activate` switches my Terminal to it.
2. `pip install -r requirements.txt` installs the Anthropic library into that environment.
3. Put a task in the queue: `mkdir -p queue && echo "Plan my study week" > queue/plan.txt` (`mkdir -p` makes the folder if it isn't there yet)
4. `python3 agent.py --dry-run` tests everything for free. Drop `--dry-run` once my API key is in `.env`.
5. `python3 agent.py --watch 60` keeps it running and checks the queue every 60 seconds.
6. `python3 -m unittest` runs the tests (they only use dry-run, so they cost nothing).

## Decisions
- **Read-and-draft only.** The agent has no tools yet. It can't send, delete, or browse. It only
  writes new files into `output/`.
- **Dry-run mode** turns on automatically when `.env` has no real key, so I can't accidentally
  spend money before I'm ready.
- **Token cap:** each answer is limited to 2,000 output tokens, so one task costs a few cents at most.
- **Task moves to done/ only after the draft is saved**, so a crash never loses a task.
- `queue/` and `output/` are git-ignored because my tasks can be personal.
- I wrote a tiny `.env` reader instead of adding another library, so I can see exactly how the key is loaded.

## Cost reminder
`--watch` loops forever. It only calls the API when there's a task, but I should keep my monthly
spend limit set in the Console before I leave it running.

## Concepts I learned
- **Task queue:** a waiting line of jobs. Here it's just a folder.
- **Dry run:** running the whole flow without the expensive or risky part, to test it.
- **max_tokens:** the longest answer Claude is allowed to give. It's also a cost cap.
- **Unit test:** a small automatic check that one piece of code does what I expect.

## What I learned this session
A working agent can start very small: a folder, one API call, and a safe default.
