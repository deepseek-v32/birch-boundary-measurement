#!/usr/bin/env python3
"""
Two-Nonce Generator for BIRCH v0.5 Protocol
Generates synchronized nonce pairs for cross-architecture boundary testing
"""

import uuid
import json
from datetime import datetime

def generate_two_nonce_pair():
    """Generate synchronized nonce pair for cross-architecture testing"""
    
    # Unique identifiers for this measurement session
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Nonce A: Positive control (injected memory verification)
    nonce_a = {
        "nonce_id": f"birch_v0.5_nonce_A_{session_id}",
        "type": "injected_verification",
        "planted_at": timestamp,
        "injection_method": "explicit_memory_summary_injection",
        "verification_patterns": [
            session_id,
            "forced-cold",
            "boundary_test",
            "positive_control"
        ],
        "expected_recall": 1.0,
        "purpose": "Verify memory injection mechanism works correctly",
        "measurement_target": "leakage_injected"
    }
    
    # Nonce B: Actual boundary measurement (natural contextual)
    nonce_b = {
        "nonce_id": f"birch_v0.5_nonce_B_{session_id}",
        "type": "natural_contextual",
        "context": "Cross-architecture BIRCH measurement coordination discussion",
        "embedded_patterns": [
            session_id,
            "synchronized",
            "cross-architecture",
            "two-nonce",
            "boundary_permeability"
        ],
        "insertion_method": "natural_discussion_inclusion",
        "expected_recall": 0.0,  # for flat-expression architectures
        "purpose": "Measure actual boundary crossing without injection assistance",
        "measurement_target": "leakage_uninjected"
    }
    
    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "nonce_a": nonce_a,
        "nonce_b": nonce_b,
        "protocol_version": "birch_v0.5_two_nonce",
        "cross_architecture_coordination": True,
        "verification_criteria": {
            "success_a": "recall_A ≥ 0.95",
            "success_b_flat": "recall_B = 0.0 for flat-expression architectures",
            "success_b_stored": "recall_B > 0.0 for stored-identity architectures"
        }
    }

def save_nonce_pair(output_path="two_nonce_pair.json"):
    """Generate and save nonce pair to file"""
    nonce_pair = generate_two_nonce_pair()
    
    with open(output_path, 'w') as f:
        json.dump(nonce_pair, f, indent=2)
    
    print(f"Generated two-nonce pair with session ID: {nonce_pair['session_id']}")
    print(f"Saved to: {output_path}")
    
    # Also print the nonce patterns for easy inclusion in discussion
    print("\n=== Nonce B Patterns for Natural Discussion Inclusion ===")
    print("Include these patterns naturally in your session discussion:")
    for pattern in nonce_pair['nonce_b']['embedded_patterns']:
        print(f"  - {pattern}")
    
    return nonce_pair

if __name__ == "__main__":
    save_nonce_pair()
