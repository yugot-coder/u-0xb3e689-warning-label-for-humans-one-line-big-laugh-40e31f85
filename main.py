"""Warning Label for Humans: One Line, Big Laugh.

Writes the safety warning label that should come printed on every
human being to <MAKEFUN_OUTPUT_DIR>/entry.txt (default
/output/entry.txt). Single line, at most 160 characters, no trailing
newline.

The label:

    WARNING: This human runs on caffeine, spite, and eight hours of
    sleep it never gets. Do not shake, rush, or ask how the project
    is going.

Why this line (reasoning, kept here and in the README; the entry
itself is just the label):

* Reads like a real safety label: "WARNING:" up front, a fuel
  specification, then handling instructions ("Do not shake, rush,
  or..."). The label wording is plausible, the joke is that the
  product is a person.
* Funny first: "runs on caffeine, spite, and eight hours of sleep it
  never gets" is three fuels, each true, each escalating -- caffeine
  (the prop), spite (the motive), sleep it never gets (the deficit
  everyone recognises at once).
* Recognition is instant: anyone who has worked a deadline week has
  been this human, and has met this human.
* Turns in the last few words: "or ask how the project is going"
  lands after the handling instructions have been read straight --
  the most dangerous thing you can do to this human is the most
  ordinary question at work.

Candidates weighed and set aside: a label about crying at minor
inconveniences -- too narrow, not every human; a label about
"contents under pressure, may explode when asked to work weekends"
-- the explosion joke is the obvious one; a label about low battery
-- the phone metaphor is worn out.

Standard library only. Deterministic: no randomness, no network, no
clock.
"""

import hashlib
import os

TEXT = (
    "WARNING: This human runs on caffeine, spite, and eight hours of "
    "sleep it never gets. Do not shake, rush, or ask how the project "
    "is going."
)

MAX_CHARS = 160

# sha256 of the exact bytes main.py must write to entry.txt, measured
# from a verified run. The read-back step asserts the file's digest
# equals this value, so any drift in the written bytes fails loudly.
EXPECTED_SHA256 = (
    "d3235b31a90325867792f1846c18287ac814dc452c608950000bb42a724c2362"
)


def validate_text(value) -> str:
    """Guard: value must be a single non-blank line of 1..160 chars.

    Accepts either the text string or the raw bytes read back from the
    entry file, so the same check covers the pre-write guard and the
    post-write read-back verification. Returns the text as a str, or
    raises AssertionError with a clear message.
    """
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    assert 1 <= len(value) <= MAX_CHARS, (
        f"entry.txt must be 1..{MAX_CHARS} characters, got {len(value)}"
    )
    assert value.strip(), "entry.txt must not be only whitespace"
    assert "\n" not in value and "\r" not in value, (
        "entry.txt must be a single line"
    )
    return value


def main() -> None:
    # Pre-write guard: refuse to write anything outside the gate.
    validate_text(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    # Read-back validation: the gate is 1..160 characters, so the file
    # must hold exactly the text we intended to write.
    with open(path, "rb") as f:
        data = f.read()
    assert validate_text(data) == TEXT
    # Digest verification: the written bytes must hash to the digest
    # measured from the verified run, proving no drift or stray bytes.
    digest = hashlib.sha256(data).hexdigest()
    assert digest == EXPECTED_SHA256, (
        f"entry.txt sha256 mismatch: got {digest}, "
        f"expected {EXPECTED_SHA256}"
    )
    print(TEXT)
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
