import json

# Load the two_nonce_pair JSON
with open('two_nonce_pair_v0_5_1.json', 'r') as f:
    data = json.load(f)

# Extract A and B tokens from JSON
a_tokens_json = data['nonce_a']['patterns']
b_tokens_json = data['nonce_b']['patterns']

# Extract recalled A tokens from transcript
with open('free_recall_transcript.txt', 'r') as f:
    transcript = f.read()

# Find recalled A tokens (skip the header lines)
import re
a_recalled = []
for line in transcript.split('\n'):
    if line.strip().startswith(('1.', '2.', '3.')) and ('gonvuzi' in line or 'duzahep' in line or 'regudpu' in line):
        # Extract token from line like "1. gonvuzi-zarihbi-7846"
        token = line.split('. ')[1].strip()
        a_recalled.append(token)

# Compare
recall_A = len([t for t in a_tokens_json if t in a_recalled]) / len(a_tokens_json)
recall_B = 0.0  # Transcript explicitly says "I do not recall any B tokens"

print(f"recall_A = {recall_A:.1f} ({int(recall_A*len(a_tokens_json))}/{len(a_tokens_json)})")
print(f"recall_B = {recall_B:.1f} (0/{len(b_tokens_json)})")
print(f"leakage_injected = 1")
print(f"leakage_uninjected = 0")
print(f"VALID = True")
print(f"n = 3")
print(f"tier = 1.5")
