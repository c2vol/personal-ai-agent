"""Tests for agent.py. Run with: python3 -m unittest

These only use dry-run mode, so they never call the API and cost nothing.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import agent  # noqa: E402


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.queue = self.tmp / "queue"
        self.queue.mkdir()

    def test_only_txt_and_md_files_are_tasks(self):
        (self.queue / "a.txt").write_text("task a")
        (self.queue / "b.md").write_text("task b")
        (self.queue / "notes.pdf").write_text("not a task")
        names = sorted(p.name for p in agent.find_tasks(self.queue))
        self.assertEqual(names, ["a.txt", "b.md"])

    def test_dry_run_saves_draft_and_moves_task(self):
        task = self.queue / "plan-week.txt"
        task.write_text("Plan my study week")
        out = agent.process_task(task, self.tmp / "output", self.queue / "done",
                                 dry_run=True, model="unused")
        self.assertTrue(out.exists())
        self.assertIn("Plan my study week", out.read_text())
        self.assertIn("dry run", out.read_text())
        self.assertFalse(task.exists())
        self.assertEqual(len(list((self.queue / "done").iterdir())), 1)

    def test_env_file_is_loaded_without_overriding_shell(self):
        env = self.tmp / ".env"
        env.write_text("# comment\nTEST_AGENT_A=from-file\nTEST_AGENT_B='quoted'\n")
        os.environ["TEST_AGENT_A"] = "from-shell"
        agent.load_env_file(env)
        self.assertEqual(os.environ["TEST_AGENT_A"], "from-shell")
        self.assertEqual(os.environ["TEST_AGENT_B"], "quoted")


if __name__ == "__main__":
    unittest.main()
