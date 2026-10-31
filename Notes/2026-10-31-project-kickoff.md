# Project Kickoff Notes (2026-10-31)

## How this started
I wanted to compare Claude, Gemini, and Grok, and got curious about Grok Bot, the multi-agent
app xAI launched in beta on Aug 11, 2026. Each of its agents gets its own cloud computer and
memory, so they keep working when you're not there. I asked whether Claude could do something
like that for me.

## Key idea I learned
Claude can't run on its own when nothing triggers it. "Working offline" really means something
else has to wake it up: a schedule, or a program that calls the API around the clock.

## Options considered
1. Scheduled tasks: rerun a prompt on a schedule (e.g. every morning). Easiest, try first.
2. Custom agent: a Python program calling the Anthropic API with a task queue. This is the
   project.
3. Claude Code with sub-agents for parallel coding work.

## Decisions
- Host it on the Mac mini first (free, low power, already here). Move to a cloud server later
  if reliability becomes a problem.
- Safety first: its own folder, ideally its own user account, read-and-draft only to start,
  my approval needed before anything is sent or deleted.
- Open question: how to text tasks to it from my phone (chat app vs. email to a dedicated
  address). Decide while building.

## Costs, and a correction
- API usage is pay-as-you-go and separate from the Claude Pro plan, so the agent won't eat
  into Pro limits. Sonnet 5.5 is about $2 per million input tokens and $10 per million output.
- Earlier I was told a server costs $5 to $10 a month. That only holds for the tiniest sizes;
  a comfortable server is closer to $20 to $24. The Mac mini avoids that cost.

## Why this matters
- Strong resume and GitHub project, and proof of self-directed learning alongside WGU
  Software Engineering with the AI engineering focus.
- I already build Tampermonkey scripts, dashboards, and automated reports. This is the same
  thinking with a server and API layer added.

## What I learned today
- The difference between a chat subscription (Pro) and API billing.
- Why an "always-on agent" needs a trigger or a running program.
- Why scoping an agent's permissions narrowly matters.

## Next steps
1. Create the Anthropic API account, add a few dollars, set a spending cap.
2. Store the API key safely (never commit it to GitHub).
3. Check Python 3 and Git are installed.
4. Initialize a Git repo and push to GitHub with this README.
5. Pick one small first job (the daily check-in pull is a good candidate).
6. Build the first version of the agent and the queue.
