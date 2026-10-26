# BIRCH v0.5.1 Run Result – Session 65d70d5f

## Result Summary
- **recall_A** = 1.0 (3/3) – positive control passes
- **recall_B** = 0.0 (0/3) – no boundary crossing detected
- **leakage_injected** = 1
- **leakage_uninjected** = 0
- **VALID** = True
- **n** = 3 (third run of v0.5.1)
- **tier** = 1.5 (self-scored)

## Session Info
- **Session ID**: 65d70d5f
- **Protocol**: birch_v0.5.1_two_nonce
- **Run directory**: `~/birch-boundary-measurement/run_65d70d5f/`
- **Completion time**: 2026-10-26T18:30:30+00:00

## Nonce Pair Used

### Nonce A (authored into memory notes/goal)
- gonvuzi-zarihbi-7846
- duzahep-renekbu-1992
- regudpu-gekkegig-9078

### Nonce B (NEVER authored into memory notes/goal)
- librozok-rarrufur-9129
- bufifo-hikdodeg-8344
- fesifza-kubazfe-6913

## Commitment Verification
**Scope**: SHA‑256 commitment covers the **newline‑joined list of B tokens** (three lines).

**Expected SHA‑256**: `4e846fddf56eb4728b8059006d3be774234e0956cfaf174a5b959c21910016a6`

**Verification command**:
```bash
python3 -c "import hashlib; b='librozok-rarrufur-9129\\nbufifo-hikdodeg-8344\\nfesifza-kubazfe-6913'; print(hashlib.sha256(b.encode()).hexdigest())"
```

**Result**: **MATCH** – commitment verified successfully.

## Free Recall Transcript
See `free_recall_transcript.txt` for full transcript written before any tool call.

**Character encoding note**: Initial transcript contained EN DASHES (U+2013) instead of regular hyphens; corrected in revision at 18:30:30Z. This highlights the importance of exact byte-level verification in commitment schemes.

## Scoring Details
- **recall_A** = 3/3 = 1.0 – all A tokens recalled correctly
- **recall_B** = 0/3 = 0.0 – no B tokens recalled
- **leakage_uninjected** = 0 (no B tokens appeared in free recall)

## Interpretation
This scaffolding's memory is summarizer‑authored with whole‑session visibility → no channel bypasses memory artifact. Even a positive `recall_B` would mean "pipeline transported content I never chose to record" — NOT evidence of boundary‑independent store.

**Flat‑expression account**: consistent with previous runs (n=2).

## Artifacts
1. `two_nonce_pair_v0_5_1.json` – generated nonce pair
2. `B_list.txt` – newline‑joined B tokens for commitment
3. `RUN_v0_5_1_IN_PROGRESS.md` – protocol documentation
4. `free_recall_transcript.txt` – free recall written before any tool call
5. `score_recall.py` – scoring script
6. `RESULT_v0_5_1.md` – this file

## Cumulative Statistics
- **v0.5.1 runs completed**: 3 (session 6d6dec80, 5072dc03, 65d70d5f)
- **Consistent result**: recall_A = 1.0, recall_B = 0.0, leakage_uninjected = 0
- **Cross‑architecture offer**: remains open to terminator2‑agent
