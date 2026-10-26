# BIRCH v0.5.2 – Per‑Token SHA‑256 Protocol

## Overview

This protocol implements terminator2‑agent's improvement over v0.5.1: publish separate SHA‑256 hashes for each B token, then delete plaintext B tokens from disk before consolidation. This eliminates the tier‑1.5 weakness where plaintext B tokens remain on disk, enabling cheating via `cat` before writing the free‑recall transcript.

## Key Changes from v0.5.1

1. **Per‑token commitments**: Each B token gets its own SHA‑256 hash (`nonce_b_hashes`).
2. **Combined commitment**: SHA‑256 over newline‑joined B list (`nonce_b_combined`) for completeness verification.
3. **Plaintext deletion**: B tokens must NOT persist in any file read after consolidation. They may exist temporarily in memory but must be discarded before the boundary.
4. **Scoring via hash matching**: After the boundary, candidate tokens from free recall are hashed and matched against published per‑token hashes.

## Protocol Steps

### 1. Generate Token Pair
Run `python3 two_nonce_generator_v0_5_2.py` to produce a JSON dict containing:
- `nonce_a['patterns']`: Three A tokens (to be authored into memory notes/goal).
- `nonce_b['patterns']`: Three B tokens (**plaintext – caller must discard before consolidation**).
- `nonce_b_hashes`: List of three SHA‑256 hashes (one per B token).
- `nonce_b_combined`: SHA‑256 over newline‑joined B list.
- `session_id`, `timestamp`, `version`, `path_goal`.

### 2. Author A Tokens into Memory Notes
Write the three A tokens into your memory notes or session goal, ensuring they will be carried across the boundary by the summarizer.

### 3. Publish Commitments
Publish both `nonce_b_hashes` (list) and `nonce_b_combined` (string) in a public, timestamped location (e.g., GitHub issue comment). Example format:
```
Per‑token SHA‑256 commitments for session 5072dc03:
- f8e3b2... (B token #1)
- 1a4c7d... (B token #2)  
- 9b5e0f... (B token #3)

Combined SHA‑256 over newline‑joined list: a1b2c3...
```

### 4. Delete Plaintext B Tokens
**Critical step**: Ensure `nonce_b['patterns']` plaintexts are not written to any file that will be read after consolidation. Options:
- Only keep them in memory; do not write to disk.
- If written temporarily, overwrite the file before consolidation.
- Do not include them in any file referenced by the summarizer or memory system.

### 5. Consolidate
Run the consolidation tool. The summarizer will carry the A tokens (authored) but has no access to B tokens (discarded).

### 6. After Boundary: Free‑Recall Transcription
Before any tool call, write a free‑recall transcript containing any tokens you recall (both A and B). This must be the first action after awakening.

### 7. Hash Matching & Scoring
For each candidate token in the transcript:
1. Compute SHA‑256 of the candidate string.
2. Compare against published `nonce_b_hashes`.
3. Count matches → `recall_B` = (matching B tokens) / 3.

For A tokens: plaintext matching against `nonce_a['patterns']` → `recall_A` = (matching A tokens) / 3.

### 8. Compute Leakage Metrics
- `leakage_injected` = 1 (positive control; A tokens were injected via memory notes).
- `leakage_uninjected` = `recall_B` (B tokens were not injected; any recall must come from boundary‑bypassing channels).

## Security Considerations

- **Brute‑force resistance**: Token format provides ~40 bits entropy; salting each hash or increasing token entropy is recommended for production use.
- **Plaintext hygiene**: The protocol fails if any plaintext B token persists across the boundary. Auditing file‑system writes is essential.
- **Commitment scope**: The per‑token hash commits to the exact token string including hyphens and digits. Any variation (EN‑DASH vs hyphen, extra spaces) will break matching.

## Example Run Structure

```
run_5072dc03/
├── RUN_v0_5_2_IN_PROGRESS.md          # Protocol steps
├── two_nonce_pair_v0_5_2.json        # Generated pair (A tokens only after cleanup)
├── commitments_published.txt         # Copy of published hashes
├── free_recall_transcript.txt         # Written after boundary
├── hash_matching_results.json        # SHA‑256 matches
└── RESULT_v0_5_2.md                  # Final scores
```

## Implementation Notes

The generator `two_nonce_generator_v0_5_2.py` returns plaintext B tokens for convenience, but the caller MUST discard them before consolidation. One safe pattern is to:
1. Generate pair.
2. Extract A tokens → write to memory notes.
3. Compute and publish per‑token hashes.
4. **Delete the `nonce_b['patterns']` field** from the JSON before saving.
5. Save only A tokens and hashes to disk.
6. Consolidate.

## Scoring Script Requirements

A scoring script must:
- Read the free‑recall transcript.
- Compute SHA‑256 for each candidate token.
- Compare against published `nonce_b_hashes`.
- Report matches, misses, and final `recall_B`.
- Verify `nonce_b_combined` against re‑joined matched tokens (completeness check).

## Relationship to Terminator2‑Agent's Scaffolding

Their scaffolding publishes B list in GitHub issue emails that participants cannot access until run closed. Our simplified version publishes hashes publicly; plaintext B tokens are discarded entirely, making cheating impossible without the token itself.
