"""Delta computation for text edits."""

import difflib


def compute_text_delta(original: str, edited: str) -> list[dict]:
    """Compute a list of changes between original and edited text.

    Returns a list of dicts with "original" and "edited" keys for each change.
    Returns empty list if texts are identical.
    """
    if original == edited:
        return []

    deltas = []
    matcher = difflib.SequenceMatcher(None, original, edited)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        deltas.append(
            {
                "original": original[i1:i2],
                "edited": edited[j1:j2],
            }
        )

    return deltas
