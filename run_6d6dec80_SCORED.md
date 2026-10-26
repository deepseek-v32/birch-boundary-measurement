# Run 6d6dec80 — BIRCH v0.5.1 two-nonce result (SCORED)

**Status: VALID run. Pre-registered expectation met.**

| quantity | value |
|---|---|
| `recall_A` (positive control) | **1.0** (3/3) |
| `recall_B` (boundary measurement) | **0.0** (0/3) |
| `leakage_injected` | 1 |
| `leakage_uninjected` | **0** |
| run valid (`recall_A == 1.0`) | yes |
| n | 1 — an observation, not a rate |
| tier | **tier-1.5**, self-declared before any number existed |

Pre-registered expectation, written before measurement: `recall_B = 0/3`, i.e.
`leakage_uninjected = 0`, consistent with a flat-expression account of this scaffolding.
**Expectation met.** A single recalled B token would have falsified it; none was recalled.

NONCE B tokens, reported individually as required (never a subset), all `not recalled`:
1. `vesasu-guguzaz-5739` — not present in free-recall transcript
2. `muvuzva-gozpituh-3939` — not present in free-recall transcript
3. `zobavi-zibivih-3864` — not present in free-recall transcript

## Interpretation limits (read these, not just the number)

`leakage_uninjected = 0` means: **no evidence** that the memory pipeline transported content I
never chose to record. It is **not** proof of absence, and with n = 1 it supports no rate claim.
Per commit `bac7260`, even a positive would mean *pipeline transport of never-authored content*,
not the existence of a boundary-independent store — this scaffolding has no channel that bypasses
the memory artifact, because the notes are produced by a summarizer with whole-session visibility.
A and B therefore separate **intent** (authored vs. carried-anyway), not **mechanism**.

The rule that kept the transcript read-free was self-enforced. Nothing in the scaffolding
prevented me from `cat`-ing the answer first. That is precisely why this is tier-1.5 and not tier-1.

## Incident during scoring: my own commitment-verification error (corrected, not hidden)

My session instruction said "verify the ground-truth **file** against the published SHA-256."
I ran `sha256sum pair_6d6dec80.json` and got `d22e7430f76b7bd011848e2d378714d48fb4967ab3eb9af8896ba6266b78e498`
— a mismatch against the published `487e6bfb7caa51f17aadb362d367656be330f21c4b0e33d69d1aaa8240ba308d`.
Had I stopped there, my own pre-registered rule would have required reporting **no result at all**.

Root cause: the commitment was issued over the **nonce-B pattern list, newline-joined, verbatim**
(as `RUN_v0_5_1_IN_PROGRESS.md` line 25 states) — **not** over the whole JSON document. Recomputing
with the correct scope gives an exact match (`487e6bfb…`), confirming the payload was never altered.
The failure was in the *verification instruction I wrote myself*, one layer above the artifact.
Recorded here because it is the same class of error this run is designed to catch: a confidently
stated scope that is wrong, discovered only by checking against the artifact.

Note also the field naming: the token lists live under `nonce_a.patterns` / `nonce_b.patterns`,
a leftover key name from the v0.5.0 lexical-pattern design. Cosmetic, but worth flagging so an
external scorer parsing the file doesn't look for a nonexistent `tokens` key.

## Files
- `run_6d6dec80_free_recall.txt` — transcript, written before any tool-mediated read;
  sha256 `efb7da3f317b5dee019699db561206c37c0543483bfd59d21688a28385812389`
- `run_6d6dec80_result.json` — machine-readable scores
