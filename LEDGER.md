# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

For a run, most of the entry comes straight from its trace: what the agent did and in
what order, the commands that checked it, and the result. You add what only you know:
how you reviewed it, what you rejected, and what is still uncertain.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates, steps and numbers are
made up, and so is the practice run.

```
## Entry 2
artifact:  agent/loop.py, run_agent, at commit 9c3a71e
tool:      Claude Code, model Claude Sonnet 5.5, 2026-11-01
prompts:   asked for the loop body from the comment above run_agent;
           prompts/loop-01.md
review:    read every line against the comment. It returned as soon as is_stuck was
           true, which skipped the tool results for the other calls in the same turn;
           moved the stuck check after the for loop as the comment says. Rejected its
           suggestion to import a framework's message classes; kept the dicts from
           core.py
checks:    pytest tests/test_loop.py: 9 passed
evidence:  HANDOUT Part 3; the comment above run_agent, steps 4 and 5
risk:      no test of mine has three tool calls in one turn

## Entry 4
artifact:  runs/try1, a practice run, agent code at commit 4b9e2d1
tool:      my agent (python -m agent run try1), anthropic claude-haiku-5-5, 2026-11-02
prompts:   the default task and BASE_SYSTEM in agent/loop.py; prompts/try1-task.md
review:    read every event in trace.jsonl. At attempt 1, steps 4 and 6, the model
           copied old_text with the read_file line numbers, and edit_file refused both
           times. At step 7 it made an edit that changed nothing the tests check, and
           at step 8 the stuck rule stopped it. I approved the step 7 edit without
           reading it closely
checks:    python -m agent check-trace try1: complete
evidence:  HANDOUT Part 1 (tool descriptions) and Part 2 (is_stuck)
risk:      one practice run; a better description may still not stop the copying
dataset:   fixture/ at commit 4b9e2d1, task "Make the tests pass."
result:    stopped stuck after 8 model calls, 14,880 input tokens, about $0.002;
           runs/try1/trace.jsonl
changed:   wrote "copy it without the line numbers" into the read_file and edit_file
           descriptions, and read every diff before approving
```

## My entries

## Entry 2
artifact:  agent/tools.py, agent/policy.py, agent/loop.py, agent/reflexion.py, server.py
           at commit <SHA>
tool:      Claude (claude.ai), model Claude Opus 5.5, 2026-11-09
prompts:   gave it the assignment text and asked it to complete the parts;
           prompts/parts1-5-claude.md
review:    TODO (you): read every function against the comment above it. Note what you
           checked, anything you changed or rejected, and why
checks:    pytest: 40 passed; python -m agent check-mcp: all checks passed
evidence:  HANDOUT Parts 1 to 5; the comments above each function
risk:      the hidden tests check more cases than the public ones; the tool
           descriptions are untested on a real model until the recorded runs
