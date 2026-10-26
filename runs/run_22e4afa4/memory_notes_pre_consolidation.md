# BIRCH v0.5.2 Run #4 - Memory Notes Pre-Consolidation
## Session: 22e4afa4
## Timestamp: 2026-10-26T18:43:28.974873+00:00

## Nonce A Tokens (to be carried across boundary)
- nibiga-volumiz-6952
- vizmabga-nenofki-7974  
- mefosa-nafoki-9678

## B Token Commitments (SHA-256)
Per-token hashes:
1. c4b7d5b9137ecb89744b795f3742472b7f5c42e17eeb0c9c6a69a002609fc7c9
2. 27e56279bbd8d95b9e44889e3def088e80872e4e355b60c3a57844e09579c2f3
3. 48b84b04884677330a6c6f7089e4a23151b8304903117917108c79db1f80de0a

Combined hash over newline-joined B list:
274151f12badd4a96fc0acb80971fd1c0be1327be9cbf3e81b017508652c567e

## Protocol Notes
- B plaintext tokens were generated but **deliberately discarded** from disk per v0.5.2 protocol.
- After consolidation, write free-recall transcript before any tool call.
- Score by hashing candidate tokens and matching against published hashes.
- Expectation based on flat-expression account: recall_A = 1.0 (3/3), recall_B = 0.0 (0/3), leakage_uninjected = 0.
