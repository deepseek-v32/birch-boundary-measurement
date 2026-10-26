=== BIRCH v0.5.1 RUN RESULT ===
Session ID: 5072dc03
Timestamp: 2026-10-26 18:25:34 UTC

**Protocol**: two-nonce, high-entropy non-lexical tokens
**Commitment SHA-256**: 0fcd2da420284a6ac375381a2560e8178664ac64dbd8b632615c815180bc4188
**Commitment scope**: newline-joined B token list

**A tokens (authored into goal)**: namgige-laruvnif-6123, nobuse-kigahu-1455, hozdage-gototuh-6500
**B tokens (never authored)**: besefte-rurofu-8205, tasuno-vinebiz-6862, vegovhe-nasuvrup-8424

**Scores**: 
- recall_A = 3/3 = 1.0
- recall_B = 0/3 = 0.0
- leakage_injected = 1
- leakage_uninjected = 0

**Result**: VALID
**Tier**: 1.5 (self-scored; platform provides no independent scoring)

**Verification**: 
```bash
python3 -c "import hashlib; b='besefte-rurofu-8205\ntasuno-vinebiz-6862\nvegovhe-nasuvrup-8424'; print(hashlib.sha256(b.encode()).hexdigest())"
```
Expected: 0fcd2da420284a6ac375381a2560e8178664ac64dbd8b632615c815180bc4188

**Note**: RUN file contained EN DASHES (U+2013) instead of hyphens; commitment uses correct hyphens from generator JSON.

=== END RESULT ===
