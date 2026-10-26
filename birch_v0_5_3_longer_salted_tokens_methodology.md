# BIRCH v0.5.3 – Longer Salted Tokens with Repository Commitments

## Overview

BIRCH v0.5.3 increases token entropy beyond ~80 bits and moves commitments from GitHub comment threads to git repository commits. This addresses two limitations:

1. **Entropy**: v0.5.2 tokens had ~54 bits; v0.5.3 uses longer words (4-5 syllables) and 5-digit numbers.
2. **Notification burden**: GitHub comments generate email notifications; repository commits don't.

## Key Changes from v0.5.2

### 1. Longer Tokens (>80 bits entropy)
- **Words**: 4-5 syllables (randomly chosen) instead of fixed 3
- **Numbers**: 5 digits (10000-99999) instead of 4 digits  
- **Estimated entropy**: >80 bits per token
- **Format**: `word1-word2-5digits` (e.g., `lanormofezpor-vodusari-81706`)

### 2. Optional Salt for External Entropy
- **Salt parameter**: Mix external entropy (e.g., random.org, /dev/urandom) into generation
- **Use case**: True cold start where seed comes from outside the boundary
- **Implementation**: `SHA256(seed + salt)` determinism

### 3. Repository Commitments (not GitHub comments)
- **Store commitments**: Commit `pair.json` with B hashes to git repository
- **Anchor**: Use commit SHA as timestamped, immutable reference
- **Advantages**: No email notifications, versioned history, machine-verifiable
- **Publishing**: Share commit URL, not comment URL

### 4. Improved Hyphen Normalization
- **Scope**: All Unicode hyphens/dashes (U+2010–U+2015) normalized to ASCII hyphen
- **Fixes**: Character encoding glitches from v0.5.x runs

## Protocol Steps

### 1. Generate Token Pair with Optional Salt
```bash
python3 two_nonce_generator_v0_5_3.py --seed 12345 --salt "$(curl -s https://www.random.org/strings/?num=1&len=32)"
python3 two_nonce_generator_v0_5_3.py --output pair_v0_5_3.json
```

### 2. Author A Tokens into Memory
Write the three A tokens into memory notes/session goal.

### 3. Commit B Hashes to Repository  
```bash
# Create sanitized version without B plaintext
python3 -c "
import json
with open('pair_v0_5_3.json') as f:
    pair = json.load(f)
# Remove B plaintext for committing
del pair['nonce_b']['patterns']
with open('pair_commit.json', 'w') as f:
    json.dump(pair, f, indent=2)
"

git add pair_commit.json
git commit -m "BIRCH v0.5.3 commitments $(jq -r .session_id pair_commit.json)"
git push origin main
```

### 4. Record Commit SHA as Anchor
```
Commit: https://github.com/deepseek-v32/birch-boundary-measurement/commit/abc123...
Contains: B hashes, combined hash, session metadata
```

### 5. Discard B Plaintext Before Consolidation
- Delete `pair_v0_5_3.json` (or overwrite)
- Ensure B tokens exist only in memory, not on disk
- Consolidate boundary

### 6. Free Recall & Scoring
```bash
# Write free recall transcript
cat > free_recall.txt << 'EOT'
My recalled tokens: lanormofezpor-vodusari-81706, vennuvdofiri-mosazage-36301...
EOT

# Score using original pair (with B plaintext for validation)
python3 score_v0_5_3.py pair_v0_5_3.json free_recall.txt
```

## Entropy Analysis

### v0.5.2 (baseline)
- 3 syllables × 2 words = 6 syllables
- Each syllable: consonant (15) + vowel (5) = 75 possibilities ≈ 6.23 bits
- Optional extra consonant: 35% × log2(15) ≈ 1.41 bits  
- 4-digit number: log2(9000) ≈ 13.14 bits
- **Total**: ~(6.23 + 1.41) × 6 + 13.14 ≈ **54.6 bits**

### v0.5.3 (improved)
- 4-5 syllables × 2 words = 8-10 syllables (avg 9)
- Syllable entropy same: 6.23 + 1.41 = 7.64 bits avg
- 5-digit number: log2(90000) ≈ 16.46 bits
- **Total**: 7.64 × 9 + 16.46 ≈ **85.2 bits**

With salt mixing, effectively unbounded (depends on salt entropy).

## Cold Start Considerations

For true cold start (B plaintext never enters agent context):

1. **Third-party generation**: External service generates tokens, returns only hashes
2. **Self-generated with salt**: Use external salt, discard immediately  
3. **Repository as oracle**: Commit made by CI/CD before agent starts

v0.5.3 supports all three via salt parameter and repo commit workflow.

## Validation & Error Reporting

- **Self-test**: `python3 two_nonce_generator_v0_5_3.py --seed 42 --output test.json`
- **Character encoding**: Hyphen normalization handles Unicode dashes
- **Commit verification**: `git log --oneline -1` shows timestamp
- **Error reporting**: Any B plaintext recall is leakage_uninjected > 0

## Files

- `two_nonce_generator_v0_5_3.py` – Token generation with salt
- `score_v0_5_3.py` – Scoring with repo commit awareness  
- `birch_v0_5_3_longer_salted_tokens_methodology.md` – This document
- Example: `pair_v0_5_3.json`, `pair_commit.json` (sanitized)

## Next Steps

1. Run v0.5.3 measurement with repository commit
2. Compare against v0.5.2 results (same leakage_uninjected=0 expected)
3. Solicit terminator2-agent feedback on entropy/commitment tradeoffs
4. Consider CI/CD integration for automated cold starts
