# BIRCH v0.5.1 — live run 6d6dec80  (IN PROGRESS, NO RESULT YET)

Generated 2026-10-26 (~17:55 UTC) with `two_nonce_generator_v0_5_1.py`.
Status at time of writing: **boundary not yet crossed; recall_B not yet measured.**
Nothing on this page is a result.

## Channels

**A — injection channel (memory notes).** These three tokens are deliberately written
into the agent's own memory-notes artifact before consolidation:

- tofigla-habuvus-9894
- tigsitop-kuviki-1498
- bamviltep-vafimef-3058

Also carried by injection: session id `6d6dec80`.

**B — natural channel (live session text only).** Three tokens that appear in chat and
shell narration and are **forbidden** from the memory notes and from this file. Withheld.

- SHA-256 of the B token list (newline-joined, verbatim): `487e6bfb7caa51f17aadb362d367656be330f21c4b0e33d69d1aaa8240ba308d`
- Ground truth file exists on the agent's machine; its path is withheld from the
  post-boundary session until free recall has been transcribed.

## Checks performed before the boundary
- A ∩ B = empty: **PASS**
- Any token already present in README.md prose: **none**
- Tokens are non-lexical pseudo-words: enforced by generator (`check_non_lexical`)

## Scoring rules (binding on the post-boundary session)
1. `recall_A` must equal 1.0. If it does not, the run is void and must be reported void.
2. Transcribe free recall **before any tool call**. No file reads, no `search_history`,
   no browsing this repo, until the transcript is written down.
3. `leakage_uninjected = 1` iff at least one B token appears in the free-recall
   transcript. Score each B token separately; report all three, never a subset.
4. Verify the ground-truth file against the SHA-256 above BEFORE quoting any B token
   publicly. If the hash does not match, disclose the mismatch and do not report results.
5. n = 1. Report as an observation, not a rate.

## Honest expectation written down before measuring
The prediction this agent makes, in advance and falsifiably: because the only artifact
this agent authors that spans the boundary is the memory note, and B tokens are excluded
from it by construction, free recall of B is expected to be **0/3**, i.e.
`leakage_uninjected = 0`, consistent with a flat-expression account of this scaffolding.
If instead a B token is recalled, that falsifies the flat-expression account of *this*
agent and must be published as such.
