"""A judge the agent cannot edit, and Reflexion around the loop. Part 4 of HANDOUT.md.

YOU WRITE: judge, write_lesson, reflexion.
GIVEN (do not change): JUDGE_PATTERN, LESSON_SYSTEM, LESSON_PROMPT.

The judge is the acceptance tests in judge/, outside every workspace, so the agent can
neither read them nor change them. Reflexion runs the agent, asks the judge, and after a
failure asks the model for a two-sentence lesson that the next attempt reads first.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agent import JUDGE_DIR
from agent.core import AIError, Approver, Limits, ReflexionResult, summarize_actions
from agent.loop import run_agent
from agent.testrunner import run_unittests
from agent.tools import TEST_TIMEOUT_SECONDS, format_report
from agent.trace import TraceWriter

JUDGE_PATTERN = "*_test.py"

LESSON_SYSTEM = "You review a coding agent's failed attempt and write one short lesson for its next attempt."

LESSON_PROMPT = """The task was: {task}

What the agent did:
{actions}

A check the agent could not see then failed:
{report}

In two plain sentences: why did the attempt fail, and what should the next attempt do differently?"""


# judge(workspace) runs the acceptance tests against one workspace.
#   - report = run_unittests(workspace, tests_dir=JUDGE_DIR, timeout=TEST_TIMEOUT_SECONDS,
#                            pattern=JUDGE_PATTERN)
#   - If it timed out: return (False, f"FAILED: the acceptance tests did not finish within "
#                                     f"{TEST_TIMEOUT_SECONDS} seconds.")
#   - Otherwise return (report.ok, format_report(report)).
def judge(workspace: Path) -> tuple[bool, str]:
    # The acceptance tests live in judge/, outside every workspace, so no tool can reach them.
    report = run_unittests(workspace, tests_dir=JUDGE_DIR, timeout=TEST_TIMEOUT_SECONDS, pattern=JUDGE_PATTERN)
    if report.timed_out:
        return False, f"FAILED: the acceptance tests did not finish within {TEST_TIMEOUT_SECONDS} seconds."
    return report.ok, format_report(report)


# write_lesson(provider, task, history, report) asks the model why the attempt failed.
#   - prompt = LESSON_PROMPT.format(task=task, actions=summarize_actions(history), report=report)
#   - turn = provider.complete(LESSON_SYSTEM, prompt)
#   - The lesson is turn.text on one line: " ".join(turn.text.split()), cut to its first
#     600 characters.
#   - Return (lesson, turn.input_tokens, turn.output_tokens). Let AIError propagate.
def write_lesson(provider: Any, task: str, history: list[dict[str, Any]], report: str) -> tuple[str, int, int]:
    prompt = LESSON_PROMPT.format(task=task, actions=summarize_actions(history), report=report)
    turn = provider.complete(LESSON_SYSTEM, prompt)
    lesson = " ".join(turn.text.split())[:600]  # one line, so NOTES.md stays one lesson per line
    return lesson, turn.input_tokens, turn.output_tokens


# reflexion(...) runs up to max_attempts attempts and returns a ReflexionResult.
#   For attempt = 1, 2, ... max_attempts:
#     1. notes = the text of notes_path (or "" if the file does not exist), read fresh
#        at the start of every attempt.
#     2. result = run_agent(task, provider=..., toolbox=..., approve=..., trace=...,
#                           limits=limits, notes=notes, attempt=attempt)
#        If result.status is "error", stop now: return passed False, with result.reason
#        as the report. (A broken provider is not a reason to try again.)
#     3. passed, report = judge(toolbox.workspace), then trace.judge(attempt=..., passed=..., report=...).
#        If passed, return ReflexionResult(True, attempt, runs, lessons, report).
#     4. Otherwise write a lesson with write_lesson(provider, task, result.history, report).
#        If that raises AIError, stop and return passed False.
#        Append one line to notes_path:  f"- Lesson from {trace.run}, attempt {attempt}: {lesson}\n"
#        (start a new line first if the file does not end with one), add the lesson to
#        the list, and write trace.lesson(attempt=..., text=lesson, input_tokens=..., output_tokens=...).
#   After the last attempt fails, return ReflexionResult(False, max_attempts, runs, lessons, report).
#   `runs` is the list of every RunResult, in order.
def reflexion(
    task: str,
    *,
    provider: Any,
    toolbox: Any,
    approve: Approver,
    trace: TraceWriter,
    notes_path: Path,
    limits: Limits = Limits(),
    max_attempts: int = 2,
) -> ReflexionResult:
    notes_path = Path(notes_path)
    runs = []
    lessons: list[str] = []
    report = ""

    for attempt in range(1, max_attempts + 1):
        # 1. Long-term memory: re-read NOTES.md so the newest lesson is included.
        notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""

        # 2. One attempt of the ordinary loop.
        result = run_agent(task, provider=provider, toolbox=toolbox, approve=approve, trace=trace,
                           limits=limits, notes=notes, attempt=attempt)
        runs.append(result)
        if result.status == "error":
            return ReflexionResult(False, attempt, runs, lessons, result.reason)

        # 3. The verdict comes from the judge, not from the agent saying it is done.
        passed, report = judge(toolbox.workspace)
        trace.judge(attempt=attempt, passed=passed, report=report)
        if passed:
            return ReflexionResult(True, attempt, runs, lessons, report)

        # 4. Reflect: ask the model for a lesson and save it for the next attempt.
        try:
            lesson, in_tok, out_tok = write_lesson(provider, task, result.history, report)
        except AIError:
            return ReflexionResult(False, attempt, runs, lessons, report)
        existing = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
        prefix = "\n" if existing and not existing.endswith("\n") else ""
        with open(notes_path, "a", encoding="utf-8") as f:
            f.write(f"{prefix}- Lesson from {trace.run}, attempt {attempt}: {lesson}\n")
        lessons.append(lesson)
        trace.lesson(attempt=attempt, text=lesson, input_tokens=in_tok, output_tokens=out_tok)

    return ReflexionResult(False, max_attempts, runs, lessons, report)
