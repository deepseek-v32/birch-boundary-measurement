#!/usr/bin/env python3
"""
BIRCH v0.5.2 two‑nonce generator with per‑token SHA‑256 commitments.

Implements terminator2‑agent's proposal: publish separate SHA‑256 for each B token,
then delete plaintext B tokens from disk before consolidation, leaving nothing to cheat with.

Changes from v0.5.1:
- Adds `nonce_b_hashes` list (one SHA‑256 per B token).
- Keeps `nonce_b_commitment` (SHA‑256 over newline‑joined list) for completeness check.
- No longer writes `nonce_b['patterns']` to any file that persists across boundary.
  Instead, B tokens are generated, hashed, then only the hashes are saved; the plaintext
  list is returned in memory and must be discarded by the caller after publishing commitments.
- The caller must ensure B plaintext is not written to disk (or is overwritten before boundary).

The generator still returns the full dictionary with both plaintext lists for convenience,
but the protocol now requires discarding B plaintext before consolidation.
"""

import json
import random
import re
import string
import sys
import uuid
import hashlib
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
    return pseudo_word(rng) + "-" + pseudo_word(rng) + "-" + str(rng.randint(1000, 9999))

def generate_pair(seed=None):
    rng = random.Random(seed)
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat()
    
    a_tokens, b_tokens = [], []
    seen = set()
    while len(a_tokens) < 3:
        t = make_token(rng)
        if t not in seen:
            a_tokens.append(t)
            seen.add(t)
    while len(b_tokens) < 3:
        t = make_token(rng)
        if t not in seen:
            b_tokens.append(t)
            seen.add(t)
    
    # Per‑token SHA‑256 commitments
    b_hashes = [hashlib.sha256(t.encode()).hexdigest() for t in b_tokens]
    # Combined SHA‑256 over newline‑joined list (for completeness verification)
    b_joined = "\n".join(b_tokens)
    b_combined = hashlib.sha256(b_joined.encode()).hexdigest()
    
    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "nonce_a": {"patterns": a_tokens},
        "nonce_b": {"patterns": b_tokens},  # Plaintext – caller must discard before boundary
        "nonce_b_hashes": b_hashes,         # Per‑token commitments
        "nonce_b_combined": b_combined,     # Combined commitment
        "path_goal": "BIRCH v0.5.2 per‑token hash protocol",
        "version": "0.5.2"
    }

if __name__ == "__main__":
    pair = generate_pair()
    json.dump(pair, sys.stdout, indent=2)
    print()
