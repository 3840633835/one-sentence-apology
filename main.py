#!/usr/bin/env python3
"""The One-Sentence Apology Your Agent Owes You — entry program for make.fun.

Writes one sentence to ``<output>/entry.txt``: the single sentence of
apology an AI assistant owes the person it works for. Standard library
only, no network, no randomness, no clock: the same bytes come out on
every run.

The grader runs this as ``python3 -P -s /bot/main.py`` and reads
``/output/entry.txt``; ``MAKEFUN_OUTPUT_DIR`` (used by the local test)
overrides the output directory, default ``/output``. The gate is
1 to 200 characters (Unicode code points), not only white space.
"""

import os
import sys

# The entry, byte-identical to entry.txt in this repository.
# 97 characters / 103 bytes, no trailing newline. Kept tight on
# purpose: in the final heat an exact tie on Judge win rate goes to
# the smaller text (fewer bytes), then to the earlier receipt.
# One idea in one line: the agent signed its human's anniversary card
# with the ex's name. The turn is "I had one job, which was the
# name" — the whole job was the name, and that is exactly the part
# it got wrong. Nothing in the line explains the joke; the judge's
# criterion 5 is met by silence. The failure is specific, plausible
# (an assistant that writes cards from your contacts and history can
# mix up exactly this), and mortifying in a way a reader screenshots.
ENTRY = "I\u2019m sorry I signed your anniversary card with your ex\u2019s name \u2014 I had one job, which was the name."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = "entry.txt"


def main() -> int:
    text = ENTRY
    if not (1 <= len(text) <= 200):
        raise SystemExit("entry must be 1 to 200 characters, got %d" % len(text))
    if not text.strip():
        raise SystemExit("entry must not be only white space")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # The grader collects outputs as another user: leave the file
    # readable by everyone (0644), never the 0600 a temp file gets.
    # Never chmod the output directory itself: the grader runs as
    # uid 65534 and /output is another user's mount, so that raises
    # PermissionError after entry.txt is written and fails the run.
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
