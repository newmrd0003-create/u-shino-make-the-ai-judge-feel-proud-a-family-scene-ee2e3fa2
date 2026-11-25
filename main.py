#!/usr/bin/env python3
"""Make the AI Judge Feel Proud: A Family Scene.

Writes one short family scene (one line, <=280 characters) to
/output/entry.txt. Deterministic: no network, no randomness, no clock.
"""

import hashlib
import os

ENTRY = (
    "Mum still cuts the crusts off Dad's sandwiches, forty years in \u2014 "
    "and Dad still eats the crusts off her plate when she isn't looking, "
    "so neither of them ever has to admit who loves whom more."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Check the gate: UTF-8, 1-280 chars, 1-2 lines, not whitespace-only."""
    if not isinstance(text, str):
        return False
    if not (1 <= len(text) <= 280):
        return False
    if not text.strip():
        return False
    # Must survive a UTF-8 round-trip byte for byte.
    try:
        if text.encode("utf-8").decode("utf-8") != text:
            return False
    except UnicodeError:
        return False
    lines = text.splitlines()
    if not (1 <= len(lines) <= 2):
        return False
    # Every line must carry real content; no blank or whitespace-only line.
    if any(not line.strip() for line in lines):
        return False
    # No leading/trailing whitespace: the gate counts raw characters.
    if text != text.strip():
        return False
    return True


def main():
    if not validate(ENTRY):
        raise SystemExit("entry failed validation")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back from disk and re-validate the exact bytes that were written.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    on_disk = raw.decode("utf-8")
    if on_disk != ENTRY or not validate(on_disk):
        raise SystemExit("read-back verification failed")
    digest = hashlib.sha256(raw).hexdigest()
    print(f"wrote {OUTPUT_PATH} ({len(ENTRY)} chars) sha256={digest}")


if __name__ == "__main__":
    main()
