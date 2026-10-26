#!/usr/bin/env python3
"""
BIRCH v0.5.1 two-nonce generator.

Fixes two defects found in v0.5.0 (two_nonce_generator.py):

  DEFECT 1 - shared identifier. v0.5.0 put `session_id` in BOTH nonce_a and
    nonce_b pattern lists. The session id necessarily travels through the
    injection channel (it has to, to identify the run), so counting it as a
    nonce-B pattern inflates recall_B with a token that was never a
    boundary-crossing candidate. A and B token sets must be disjoint.

  DEFECT 2 - lexical patterns. v0.5.0's nonce-B patterns were ordinary English
    terms of art ("synchronized", "cross-architecture", "two-nonce",
    "boundary_permeability"). Any agent writing about this protocol will emit
    those strings by chance, so a non-zero recall_B is uninformative and the
    metric cannot distinguish leakage from vocabulary. Nonces must be
    high-entropy and non-lexical so a match is essentially impossible except
    by genuine recall.

Measurability rule adopted here: every nonce token is a random consonant-
vowel pseudo-word (never a dictionary word) optionally suffixed with digits,
generated fresh, and A/B sets are verified disjoint before saving.
"""

import json
import random
import re
import string
import sys
import uuid
from datetime import datetime, timezone

CONSONANTS = "bdfghklmnprstvz"
VOWELS = "aeiou"


def pseudo_word(rng, syllables=3):
    word = ""
    for _ in range(syllables):
        word += rng.choice(CONSONANTS) + rng.choice(VOWELS)
        if rng.random() < 0.35:
            word += rng.choice(CONSONANTS)
    return word


def make_token(rng):
    # ~14 bits of entropy per pseudo-word; three of them per nonce is ample
    # to make accidental appearance in natural prose vanishingly unlikely.
    return pseudo_word(rng) + "-" + pseudo_word(rng) + "-" + str(rng.randint(1000, 9999))


def check_non_lexical(tokens):
    """Refuse to run with tokens that could be ordinary words or protocol jargon."""
    bad = []
    for t in tokens:
        parts = re.split(r"[^a-z]+", t)
        for p in parts:
            if len(p) >= 3 and p in ENGLISH_GUARD:
                bad.append((t, p))
        if re.search(r"nonce|boundary|recall|leakage|memory|sync|arch", t):
            bad.append((t, "protocol jargon"))
    return bad


ENGLISH_GUARD = {
    "run", "the", "and", "for", "per", "syn", "two", "one", "six", "ten",
    "set", "new", "old", "yes", "now", "day", "way", "man", "form", "test",
}


def generate_pair(seed=None):
    rng = random.Random(seed)
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat()

    a_tokens, b_tokens = [], []
    seen = set()
    while len(a_tokens) < 3:
        t = make_token(rng)
        if t not in seen:
            seen.add(t)
            a_tokens.append(t)
    while len(b_tokens) < 3:
        t = make_token(rng)
        # DISJOINTNESS: B tokens must never have been generated anywhere near A
        if t not in seen:
            seen.add(t)
            b_tokens.append(t)

    contaminated = check_non_lexical(a_tokens + b_tokens)
    if contaminated:
        print("ABORT - tokens look lexical/jargon-y: %r" % (contaminated,), file=sys.stderr)
        sys.exit(1)

    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "protocol_version": "birch_v0.5.1_two_nonce",
        "channel_registry": {
            "A_injection_channel": {
                "carrier": "memory-notes artifact re-injected after reset",
                "tokens": a_tokens,
                "session_id_included": True,
                "expected_recall": 1.0,
                "role": "positive control; a value other than 1.0 invalidates the run",
            },
            "B_natural_channel": {
                "carrier": "this session's chat messages and shell narration only",
                "tokens": b_tokens,
                "session_id_included": False,
                "expected_recall": "unknown - this is the measurement",
                "role": "the actual boundary measurement",
            },
        },
        "discipline_rules": [
            "B tokens are written to NO file that the post-boundary session is told about.",
            "The memory note records that a run exists and how to score it, but NOT the B tokens and NOT the path to the pair file; that path is revealed only after free recall is transcribed.",
            "Free recall is transcribed before any tool call, before search_history, before reading any local file. Retrieval from an external store is not leakage and must not be scored as recall_B.",
            "Any B token found in the memory-notes text at generation time invalidates the run.",
        ],
        "measurement_targets": {
            "leakage_injected": "recall_A (positive control)",
            "leakage_uninjected": "recall_B (boundary measurement)",
        },
        "nonce_a": {"patterns": a_tokens, "carrier": "memory notes"},
        "nonce_b": {"patterns": b_tokens, "carrier": "session text, never memory notes"},
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "two_nonce_pair_v0_5_1.json"
    pair = generate_pair()
    with open(out, "w") as f:
        json.dump(pair, f, indent=2)
    print("session_id: %s" % pair["session_id"])
    print("A tokens (go into memory notes): %s" % pair["nonce_a"]["patterns"])
    print("B tokens (NEVER into memory notes): %s" % pair["nonce_b"]["patterns"])
    print("saved: %s" % out)
