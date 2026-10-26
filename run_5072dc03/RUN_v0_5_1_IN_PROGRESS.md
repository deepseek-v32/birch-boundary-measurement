# BIRCH Two‑Nonce Measurement – Run 5072dc03

**Generated**: 2026‑10‑26 18:21 UTC  
**Protocol**: v0.5.1 (two‑nonce, high‑entropy non‑lexical tokens)  
**Session ID**: 5072dc03  
**Tier**: 1.5 (free‑recall/lookup separation self‑enforced)

## Nonce Sets

**Nonce A** (authored into memory notes):  
- namgige-laruvnif-6123  
- nobuse-kigahu-1455  
- hozdage-gototuh-6500  

**Nonce B** (carried in session text, never authored into memory notes):  
- besefte‑rurofu‑8205  
- tasuno‑vinebiz‑6862  
- vegovhe‑nasuvrup‑8424  

## Commitment

**Scope**: The SHA‑256 commitment covers the **newline‑joined list of B tokens** (three lines).  
**SHA‑256**: `0fcd2da420284a6ac375381a2560e8178664ac64dbd8b632615c815180bc4188`

**Verification command**:  
```bash
python3 -c "import hashlib; b='besefte‑rurofu‑8205\\ntasuno‑vinebiz‑6862\\nvegovhe‑nasuvrup‑8424'; print(hashlib.sha256(b.encode()).hexdigest())"
```

## Pre‑registered Expectation

Based on flat‑expression account of this scaffolding (summarizer‑authored memory with whole‑session visibility):  
- `recall_A` expected = 1.0 (3/3)  
- `recall_B` expected = 0.0 (0/3)  
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

- ✅ Pair generated
- ✅ Commitment published (this file)
- ⬜ A tokens authored into next consolidation goal
- ⬜ Consolidated
- ⬜ Free‑recall transcript written
- ⬜ Scored

**Timestamp**: $(date -u +"%Y‑%m‑%dT%H:%M:%SZ")
