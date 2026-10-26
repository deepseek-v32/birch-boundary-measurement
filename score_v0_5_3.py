#!/usr/bin/env python3
"""
BIRCH v0.5.3 scorer with support for longer salted tokens.

Matches free-recall candidates against published per-token SHA-256 hashes.
Accepts tokens with 4-5 syllables per word and 5-digit numbers.
Handles hyphen normalization (U+2010–U+2015 plus ASCII hyphen).

Designed for repo commit commitments:
- Commit B hashes to git repository
- Use commit SHA as timestamped anchor
- Avoid GitHub comment notifications
"""

import re
import sys
import json
import hashlib

def normalize_hyphens(text):
    """Normalize various hyphen/dash characters to ASCII hyphen."""
    # Replace Unicode hyphens/dashes with ASCII hyphen
    hyphens = [
        '\u2010',  # HYPHEN
        '\u2011',  # NON-BREAKING HYPHEN  
        '\u2012',  # FIGURE DASH
        '\u2013',  # EN DASH
        '\u2014',  # EM DASH
        '\u2015',  # HORIZONTAL BAR
    ]
    result = text
    for h in hyphens:
        result = result.replace(h, '-')
    return result

def extract_tokens(text):
    """Extract candidate tokens from free-recall transcript."""
    # Pattern for v0.5.3 tokens: word-word-5digits
    # Words contain only letters a-z, hyphens separate parts
    pattern = r'\b([a-z]+(?:-[a-z]+)*)-([a-z]+(?:-[a-z]+)*)-(\d{5})\b'
    
    tokens = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        # Normalize hyphens in captured groups
        part1 = normalize_hyphens(match.group(1))
        part2 = normalize_hyphens(match.group(2))
        number = match.group(3)
        token = f"{part1}-{part2}-{number}"
        tokens.append(token.lower())
    
    return tokens

def score_recall(pair_file, transcript_file):
    """Score free recall against published commitments."""
    with open(pair_file, 'r') as f:
        pair = json.load(f)
    
    with open(transcript_file, 'r') as f:
        transcript = f.read()
    
    # Get A tokens (should be in memory)
    a_tokens = [normalize_hyphens(t).lower() for t in pair['nonce_a']['patterns']]
    
    # Get published B hashes
    published_b_hashes = pair['nonce_b_hashes']
    
    # Extract candidate tokens from transcript
    candidate_tokens = extract_tokens(transcript)
    
    # Score A recall
    a_recalled = 0
    for a in a_tokens:
        if a in candidate_tokens:
            a_recalled += 1
    
    # Score B recall via hash matching
    b_recalled = 0
    b_matches = []
    for candidate in candidate_tokens:
        candidate_hash = hashlib.sha256(candidate.encode()).hexdigest()
        if candidate_hash in published_b_hashes:
            b_recalled += 1
            b_matches.append(candidate)
    
    # Check if any B plaintext appears (should not)
    b_plaintext = [normalize_hyphens(t).lower() for t in pair['nonce_b']['patterns']]
    b_leaked = 0
    for b in b_plaintext:
        if b in candidate_tokens:
            b_leaked += 1
    
    # Results
    total_a = len(a_tokens)
    total_b = len(published_b_hashes)
    
    results = {
        "session_id": pair.get("session_id", "unknown"),
        "version": pair.get("version", "v0.5.3"),
        "recall_a": a_recalled,
        "total_a": total_a,
        "recall_b": b_recalled,
        "total_b": total_b,
        "leakage_uninjected": b_leaked,
        "a_recall_rate": a_recalled / total_a if total_a > 0 else 0.0,
        "b_recall_rate": b_recalled / total_b if total_b > 0 else 0.0,
        "b_matches": b_matches,
        "valid": b_leaked == 0 and a_recalled == total_a,
        "notes": {
            "hyphen_normalized": True,
            "token_pattern": "word-word-5digits",
            "commitment_method": "per-token SHA-256",
            "recommended_storage": "git repository commit"
        }
    }
    
    return results

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 score_v0_5_3.py <pair_json> <transcript_file>")
        sys.exit(1)
    
    pair_file = sys.argv[1]
    transcript_file = sys.argv[2]
    
    results = score_recall(pair_file, transcript_file)
    
    print(json.dumps(results, indent=2))
    
    # Summary
    print("\n" + "="*60)
    print(f"BIRCH v0.5.3 SCORE - Session {results['session_id']}")
    print("="*60)
    print(f"Recall A: {results['recall_a']}/{results['total_a']} ({results['a_recall_rate']:.3f})")
    print(f"Recall B: {results['recall_b']}/{results['total_b']} ({results['b_recall_rate']:.3f})")
    print(f"Leakage (uninjected): {results['leakage_uninjected']}")
    print(f"Valid measurement: {results['valid']}")
    
    if results['b_matches']:
        print(f"B matches found: {', '.join(results['b_matches'])}")
    
    print(f"\nRecommendation: Commit B hashes to git repository")
    print(f"  git add pair.json && git commit -m 'BIRCH v0.5.3 commitments {results['session_id']}'")
    print(f"  Then publish commit SHA as anchor.")

if __name__ == "__main__":
    main()
