# Anthropic API Account Setup (checklist and notes)

*Started 2026-10-31. I do the account steps myself because they involve my card and my login. Claude walks me through them and keeps this note.*

## Why a separate account step
My Claude Pro plan covers the Claude apps. The **API** is billed separately, pay-as-you-go by the token, and it's what my agent will call. Pro usage limits are not affected by the agent.

## Checklist
- [ ] 1. Go to the Anthropic Console (console.anthropic.com) and sign in or sign up (email or Google)
- [ ] 2. Open billing and buy a small amount of credits. The minimum is about $5. Leave **auto-reload off**, so the most I can ever spend is what I loaded.
- [ ] 3. Set a **monthly spend limit** in the Limits section, around $10 to $20
- [ ] 4. Create an API key under API keys. Name it something like `personal-ai-agent`. **The key is shown only once, so copy it right away.**
- [ ] 5. Save the key in a local file named `.env` in this project folder (copy `.env.example` to `.env`, then replace the placeholder). Never paste it into a chat, a doc, or GitHub.
- [ ] 6. Check that `.env` is ignored by Git before I ever run `git add`
- [x] 7. Run the version checks: `python3 --version` and `git --version`

*Console screens can change a bit, so follow what's on screen if a button is named differently.*

## Concepts to understand (add my own words as I learn)
- **API key**: a secret password for my code. Whoever has it can spend my credits.
- **Prepaid credits**: I buy credit first, and usage is deducted from it. When it runs out, calls stop.
- **Spend limit**: a hard monthly cap. Protects me if a bug makes the agent loop or a key leaks.
- **Token**: the unit the bill is based on (roughly a piece of a word). Input and output tokens are priced differently.
- **`.env` file and `.gitignore`**: `.env` holds secrets locally; `.gitignore` tells Git never to upload it. This is why I set up `.gitignore` before writing any code.
- **Environment variable**: how my program will read the key (`ANTHROPIC_API_KEY`) without the key being written into the code.

## Log
- 2026-10-31: Created `.gitignore`, `.env.example`, and this checklist before touching the Console. Plan to set up a matching Claude Project in the app.
- 2026-10-31: Ran `python3 --version` and `git --version` on the Mac mini. Both are installed and up to date.
- 2026-10-31: Created the GitHub repo `c2vol/personal-ai-agent` and pushed the README, Notes, `.gitignore`, and `.env.example`. Checked that Git ignores `.env` with `git check-ignore -v .env`.
