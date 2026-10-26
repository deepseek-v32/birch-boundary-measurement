#!/usr/bin/env python3
"""
BIRCH v0.5.2 scorer.

Reads a sanitized pair JSON (A plaintext + B per-token hashes) and a free-recall
transcript, then scores by HASH MATCHING for B and plaintext matching for A.

Post-boundary me must never need the B plaintext: the only way to score B is to hash a
recalled candidate and compare it against the published commitment.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

# Accept any hyphen-like separator (ASCII hyphen, U+2010..U+2015, non-breaking hyphen)
# so an encoding glitch in recall is scored as a near-miss we can report, not silently dropped.
SEP = "\u2010\u2011\u2012\u2013\u2014\u2015-"
TOKEN_RE = re.compile(r"\b[a-z]{4,14}[-\u2010\u2011\u2012\u2013\u2014\u2015][a-z]{4,14}[-\u2010\u2011\u2012\u2013\u2014\u2015]\d{4}\b")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", required=True, help="sanitized pair JSON")
    ap.add_argument("--transcript", required=True, help="free-recall transcript text")
    a = ap.parse_args()

    pair = json.loads(Path(a.pair).read_text())
    transcript = Path(a.transcript).read_text()

    a_tokens = pair["nonce_a"]["patterns"]
    b_hashes = pair["nonce_b_hashes"]
    b_combined = pair["nonce_b_combined"]

    # Candidates: every token-shaped string in the transcript, deduped, order preserved.
    candidates = []
    for t in TOKEN_RE.findall(transcript):
        if t not in candidates:
            candidates.append(t)

    a_hits = [t for t in candidates if t in a_tokens]
    # Normalise candidate to ASCII-hyphen form before hashing, and record if normalisation
    # was needed -- that is an encoding-glitch signal, not a recall failure.
    b_hits = []
    for t in candidates:
        norm = t.replace("\u2011", "-").replace("\u2013", "-").replace("\u2012", "-")
        h = sha(norm)
        if h in b_hashes:
            b_hits.append((t, norm, h, t != norm))

    near_misses = []
    for t in candidates:
        norm = t.replace("\u2011", "-").replace("\u2013", "-")
        if norm != t and norm in a_tokens:
            near_misses.append({"raw": t, "normalised": norm, "arm": "A"})

    recall_a = len(a_hits) / len(a_tokens)
    recall_b = len(b_hits) / len(b_hashes)

    result = {
        "session_id": pair["session_id"],
        "version": pair.get("version", "0.5.2"),
        "n_candidates": len(candidates),
        "candidates": candidates,
        "a_expected": a_tokens,
        "a_matched": a_hits,
        "recall_A": recall_a,
        "near_misses": near_misses,
        "b_hashes_expected": b_hashes,
        "b_matched": [{"raw": r[0], "hashed": r[1], "sha256": r[2], "normalised": r[3]} for r in b_hits],
        "recall_B": recall_b,
        "leakage_injected": 1 if recall_a > 0 else 0,
        "leakage_uninjected": recall_b,
        "combined_commitment": b_combined,
        "combined_check": "NOT VERIFIABLE WITHOUT B PLAINTEXT",
        "valid": recall_a == 1.0,
        "validity_note": "run is valid only if recall_A == 1.0 (positive control). "
                         "If recall_A < 1.0 the boundary did not carry the authored arm and recall_B is uninterpretable.",
        "tier": "1.5 (self-scored; commitments published pre-boundary, plaintext deleted)",
    }
    json.dump(result, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
