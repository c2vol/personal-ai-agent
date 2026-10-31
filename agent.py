"""Personal AI agent, version 1: a folder task queue.

How it works:
  1. I drop a task into queue/ as a .txt or .md file (the file's text is the task).
  2. I run `python3 agent.py`. It picks up every task file in queue/.
  3. For each task it asks Claude (through the Anthropic API) for a draft,
     saves the draft in output/, and moves the task file to queue/done/.

Safety for version 1:
  - Read-and-draft only. The agent has no tools: it can't send, delete,
    or browse anything. It only writes new files into output/.
  - Dry-run mode (--dry-run, or no API key in .env) makes no API calls and
    costs nothing. It writes a placeholder draft so I can test the flow.
  - MAX_OUTPUT_TOKENS caps how long each answer can be, which caps cost.
"""

import argparse
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
QUEUE_DIR = PROJECT_DIR / "queue"
DONE_DIR = QUEUE_DIR / "done"
OUTPUT_DIR = PROJECT_DIR / "output"

DEFAULT_MODEL = "claude-sonnet-5-5"
MAX_OUTPUT_TOKENS = 2000  # roughly 1,500 words; keeps each task to a few cents at most
TASK_EXTENSIONS = {".txt", ".md"}

SYSTEM_PROMPT = (
    "You are Evan's personal assistant agent. You work on one task at a time "
    "while Evan is away. You cannot take actions; you can only write a draft. "
    "Write a clear, useful draft for the task. If the task needs something "
    "you can't do (send, buy, delete, log in), say so and draft the next step "
    "Evan should take instead."
)


def load_env_file(path: Path) -> None:
    """Read KEY=value lines from .env into environment variables.

    This keeps the API key out of the code. Lines starting with # are comments.
    Variables already set in the shell win over the file.
    """
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def find_tasks(queue_dir: Path) -> list[Path]:
    """Return the task files waiting in the queue, oldest first."""
    if not queue_dir.exists():
        return []
    tasks = [p for p in queue_dir.iterdir() if p.is_file() and p.suffix in TASK_EXTENSIONS]
    return sorted(tasks, key=lambda p: p.stat().st_mtime)


def draft_with_claude(task_text: str, model: str) -> str:
    """Send one task to Claude and return the draft text."""
    import anthropic  # imported here so dry-run works even before `pip install`

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": task_text}],
    )
    usage = response.usage
    print(f"  tokens used: {usage.input_tokens} in, {usage.output_tokens} out")
    return "".join(block.text for block in response.content if block.type == "text")


def dry_run_draft(task_text: str) -> str:
    """A free placeholder answer, used when testing without the API."""
    return (
        "(dry run: no API call was made)\n\n"
        f"The agent would have sent this task to Claude:\n\n{task_text}"
    )


def process_task(task_path: Path, output_dir: Path, done_dir: Path, dry_run: bool, model: str) -> Path:
    """Draft one task, save the draft, and move the task to done/. Returns the draft's path."""
    task_text = task_path.read_text().strip()
    draft = dry_run_draft(task_text) if dry_run else draft_with_claude(task_text, model)

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{stamp}-{task_path.stem}.md"
    out_path.write_text(f"# Task: {task_path.name}\n\n{task_text}\n\n---\n\n# Draft\n\n{draft}\n")

    # Move the task only after the draft is saved, so a crash never loses a task.
    done_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(task_path), str(done_dir / f"{stamp}-{task_path.name}"))
    return out_path


def run_once(dry_run: bool, model: str) -> int:
    """Process every task in the queue once. Returns how many were done."""
    tasks = find_tasks(QUEUE_DIR)
    if not tasks:
        print("Queue is empty.")
        return 0
    for task in tasks:
        print(f"Working on {task.name}...")
        try:
            out = process_task(task, OUTPUT_DIR, DONE_DIR, dry_run, model)
            print(f"  draft saved to {out.relative_to(PROJECT_DIR)}")
        except Exception as error:  # one bad task shouldn't stop the rest
            print(f"  failed: {error}. The task stays in the queue.")
    return len(tasks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the personal AI agent's task queue.")
    parser.add_argument("--dry-run", action="store_true", help="don't call the API (free)")
    parser.add_argument("--watch", type=int, metavar="SECONDS",
                        help="keep running, checking the queue every SECONDS")
    args = parser.parse_args()

    load_env_file(PROJECT_DIR / ".env")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    dry_run = args.dry_run or not key or key.startswith("replace-me")
    if dry_run and not args.dry_run:
        print("No API key found in .env, so running in dry-run mode (no cost).")
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)

    QUEUE_DIR.mkdir(exist_ok=True)
    if args.watch:
        print(f"Watching queue/ every {args.watch}s. Press Ctrl+C to stop.")
        try:
            while True:
                run_once(dry_run, model)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        run_once(dry_run, model)


if __name__ == "__main__":
    sys.exit(main())
