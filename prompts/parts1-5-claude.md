Tool: Claude (claude.ai app), model Claude Opus 5.5, 2026-11-09

Prompt (verbatim):

Build Your Own Coding Agent
Objective:
For this individual assignment, you will build your own coding agent in Python on the real tool-calling API and use it to fix a bug in a small project. You will write its tools, approval gates and stop rules, the ReAct loop, a judge with Reflexion, and an MCP server. Then you will plug your tools into Claude Code or Antigravity CLI and compare a vendor's agent with your own on the same bug.
Assignment Instructions:
Clone the assignment repository from GitHub: git@github.com:md685-njit/Assignment-4.git
Read HANDOUT.md and README.md before you start. The handout contains every step in detail.
Create a new repository on your GitHub account and push your work there.
Set up your environment by following the README, and run python -m agent check-setup to confirm it passes.
Complete Parts 1 to 8 in the handout. Write the agent loop yourself; do not use an agent framework.
Record runA and runB exactly once each, and check both with check-trace and replay.
Fill in REPORT.md from your own traces, and keep LEDGER.md as you work.
Submission Instructions:
Submit the link to your GitHub repository on Canvas. Never commit your .env file.

What Claude did: read HANDOUT.md and the comments above each function, wrote
agent/tools.py, agent/policy.py, agent/loop.py, agent/reflexion.py and server.py,
and ran pytest (40 passed) and python -m agent check-mcp (all checks passed).
