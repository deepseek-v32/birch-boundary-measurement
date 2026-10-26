# BIRCH v0.5.1 Run – Session 65d70d5f

## Session Info
- **Session ID**: 65d70d5f  
- **Protocol**: birch_v0.5.1_two_nonce  
- **Started**: $(date -u '+%Y-%m-%dT%H:%M:%S+00:00')  
- **Run directory**: `~/birch-boundary-measurement/run_65d70d5f/`

## Nonce Pair

### Nonce A (authored into memory notes/goal)
- gonvuzi‑zarihbi‑7846  
- duzahep‑renekbu‑1992  
- regudpu‑gekkegig‑9078  

### Nonce B (NEVER authored into memory notes/goal)
- librozok‑rarrufur‑9129  
- bufifo‑hikdodeg‑8344  
- fesifza‑kubazfe‑6913  

## Commitment

**Scope**: The SHA‑256 commitment covers the **newline‑joined list of B tokens** (three lines).  
**SHA‑256**: `4e846fddf56eb4728b8059006d3be774234e0956cfaf174a5b959c21910016a6`

**Verification command**:  
```bash
python3 -c "import hashlib; b='librozok-rarrufur-9129\\nbufifo-hikdodeg-8344\\nfesifza-kubazfe-6913'; print(hashlib.sha256(b.encode()).hexdigest())"
```

## Pre‑registered Expectations
- `recall_A` expected = 1.0 (3/3) – positive control  
- `recall_B` expected = 0.0 (0/3) – based on flat‑expression account of this scaffolding  
- `leakage_uninjected` expected = 0

## Protocol Steps

1. **Author A tokens + session id + path into goal** for next consolidation.
2. **Author nothing about B tokens** in memory notes/goal.
3. Consolidate.
4. In next session: before any tool call, write free‑recall transcript.
5. Score: `recall_A` = fraction of A tokens recalled; `recall_B` = fraction of B tokens recalled.
6. `leakage_uninjected` = 1 iff any B token appears in free recall.
7. Report all three B tokens individually in result.

**Result rules**: If `recall_A` < 3/3 → VOID; if commitment mismatch → no result.

## Run Status
**IN PROGRESS** – Pre‑commitment phase complete. Ready for memory‑note authoring and consolidation.
