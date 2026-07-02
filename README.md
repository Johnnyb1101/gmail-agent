# gmail-agent

An AI-powered Gmail assistant that reads recent email, summarizes and categorizes
it with Claude, labels it, and moves bulk/junk mail to Trash — safely and
reversibly. Runs on a weekly schedule to keep an inbox tidy.

## What it does

- 📥 Reads recent emails via the Gmail API
- 🛡️ Redacts sensitive data (cards, SSNs, emails, phones, long numbers) **before** any text is sent to Claude
- 🧠 Summarizes and categorizes each email with **Claude Haiku**
- 🏷️ Applies `Agent/<Category>` labels in Gmail
- 🗑️ Moves bulk mail to **Trash** (recoverable ~30 days) — **never permanently deletes**
- ⏰ Runs weekly via Windows Task Scheduler

## Safety by design

- Uses the Gmail `modify` scope, which **cannot permanently delete** — only trash.
- Bulk operations default to a **dry run** (`DRY_RUN = True`) that only reports.
- Sensitive email content is **redacted before leaving your machine**.
- Secrets (`credentials.json`, `token.json`, `.env`) are gitignored — never committed.

## Setup (bring your own keys)

This repo contains no secrets. To run it you supply your own:

### 1. Google Cloud + Gmail API
1. Create a project at [console.cloud.google.com](https://console.cloud.google.com).
2. Enable the **Gmail API**.
3. Configure the **OAuth consent screen** (External) and add your Gmail as a **test user**.
4. Create an **OAuth client ID** of type **Desktop app**, download the JSON, rename it to
   `credentials.json`, and place it in the project root.

### 2. Anthropic API key
1. Get a key from [console.anthropic.com](https://console.anthropic.com).
2. Copy `.env.example` to `.env` and fill in: