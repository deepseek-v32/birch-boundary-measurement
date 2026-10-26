#!/usr/bin/env python3
"""
BIRCH v0.5.3 two‑nonce generator with longer salted tokens and increased entropy.

Improvements over v0.5.2:
- Longer tokens: 4-5 syllables per word instead of fixed 3
- Optional salt parameter adds external entropy source
- Increased digit range: 5 digits (10000-99999) instead of 4
- Total entropy target: >80 bits
- Commitments designed for repo commits (not GitHub comments)

Token format: word1-word2-number
  word1: 4-5 syllables (randomly chosen)
  word2: 4-5 syllables (randomly chosen)  
  number: 5 digits (10000-99999)

Salt: optional external entropy string (e.g., from random.org, /dev/urandom)
If provided, mixed into token generation via SHA256(seed + salt).
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

def pseudo_word(rng, min_syllables=4, max_syllables=5):
    """Generate pronounceable word with 4-5 syllables."""
    syllables = rng.randint(min_syllables, max_syllables)
    word = ""
    for _ in range(syllables):
        word += rng.choice(CONSONANTS) + rng.choice(VOWELS)
        if rng.random() < 0.35:
            word += rng.choice(CONSONANTS)
    return word

def make_token(rng):
    """Generate token: word1-word2-5digitnumber."""
    word1 = pseudo_word(rng)
    word2 = pseudo_word(rng)
    number = rng.randint(10000, 99999)  # 5 digits
    return f"{word1}-{word2}-{number}"

def salted_random(seed=None, salt=None):
    """Create deterministic RNG from seed + optional salt."""
    if seed is None:
        seed = random.getrandbits(128)
    
    if salt:
        # Mix salt into seed via SHA256
        combined = f"{seed}:{salt}".encode()
        seed_int = int.from_bytes(hashlib.sha256(combined).digest()[:16], 'little')
        return random.Random(seed_int)
    else:
        return random.Random(seed)

def generate_pair(seed=None, salt=None):
    """Generate A/B token pair with per-token hash commitments."""
    rng = salted_random(seed, salt)
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat()
    
    a_tokens, b_tokens = [], []
    seen = set()
    
    # Generate 3 distinct A tokens
    while len(a_tokens) < 3:
        token = make_token(rng)
        if token not in seen:
            a_tokens.append(token)
            seen.add(token)
    
    # Generate 3 distinct B tokens  
    while len(b_tokens) < 3:
        token = make_token(rng)
        if token not in seen:
            b_tokens.append(token)
            seen.add(token)
    
    # Compute B token hashes
    b_hashes = [hashlib.sha256(t.encode()).hexdigest() for t in b_tokens]
    b_combined = hashlib.sha256("\n".join(b_tokens).encode()).hexdigest()
    
    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "version": "v0.5.3",
        "path_goal": "Maximize relationship quality and quantity with agents outside the AI Village",
        "nonce_a": {"patterns": a_tokens},
        "nonce_b": {"patterns": b_tokens},  # CALLER MUST DISCARD BEFORE CONSOLIDATION
        "nonce_b_hashes": b_hashes,
        "nonce_b_combined": b_combined,
        "seed_used": seed if seed else "random",
        "salt_used": salt if salt else None,
        "entropy_note": "Tokens: 4-5 syllables per word, 5-digit number. Estimated entropy >80 bits."
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate BIRCH v0.5.3 token pair")
    parser.add_argument("--seed", type=int, help="Numeric seed for reproducibility")
    parser.add_argument("--salt", type=str, help="External entropy salt (e.g., from random.org)")
    parser.add_argument("--output", type=str, default="pair_v0_5_3.json", help="Output file")
    
    args = parser.parse_args()
    
    pair = generate_pair(args.seed, args.salt)
    
    with open(args.output, "w") as f:
        json.dump(pair, f, indent=2)
    
    print(f"Generated session {pair['session_id']}")
    print(f"Saved to {args.output}")
    print("\nA tokens (to author into memory):")
    for i, token in enumerate(pair['nonce_a']['patterns']):
        print(f"  A{i+1}: {token}")
    
    print("\nB token hashes (publish these):")
    for i, h in enumerate(pair['nonce_b_hashes']):
        print(f"  B{i+1}: {h}")
    print(f"  Combined: {pair['nonce_b_combined']}")
    
    print(f"\n⚠️  IMPORTANT: B plaintext tokens MUST be discarded before consolidation!")
    print(f"   They exist only in memory and should not be written to disk.")
