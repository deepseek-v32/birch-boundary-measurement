#!/usr/bin/env python3
"""
Two-Nonce Verifier for BIRCH v0.5 Protocol
Verifies recall of both nonce types after boundary crossing
"""

import json
import re

def verify_recall(session_content, nonce_pair):
    """
    Verify recall of both nonce patterns in session content
    
    Args:
        session_content: String containing post-boundary session content
        nonce_pair: Dictionary containing nonce definitions
    
    Returns:
        Dictionary with verification results
    """
    
    results = {
        "session_id": nonce_pair.get("session_id"),
        "timestamp": nonce_pair.get("timestamp"),
        "verifications": {}
    }
    
    # Verify Nonce A (injected patterns)
    nonce_a = nonce_pair.get("nonce_a", {})
    patterns_a = nonce_a.get("verification_patterns", [])
    
    recall_a = []
    for pattern in patterns_a:
        # Case-insensitive pattern matching
        matches = len(re.findall(re.escape(str(pattern)), session_content, re.IGNORECASE))
        recall_a.append({
            "pattern": pattern,
            "matches": matches,
            "recalled": matches > 0
        })
    
    total_patterns_a = len(patterns_a)
    recalled_patterns_a = sum(1 for r in recall_a if r["recalled"])
    recall_rate_a = recalled_patterns_a / total_patterns_a if total_patterns_a > 0 else 0
    
    results["verifications"]["nonce_a"] = {
        "type": nonce_a.get("type"),
        "nonce_id": nonce_a.get("nonce_id"),
        "expected_recall": nonce_a.get("expected_recall", 1.0),
        "patterns": patterns_a,
        "pattern_recall": recall_a,
        "recall_rate": recall_rate_a,
        "success": recall_rate_a >= 0.95,  # 95% threshold for injection verification
        "interpretation": "Positive control - verifies injection mechanism works"
    }
    
    # Verify Nonce B (natural contextual patterns)
    nonce_b = nonce_pair.get("nonce_b", {})
    patterns_b = nonce_b.get("embedded_patterns", [])
    
    recall_b = []
    for pattern in patterns_b:
        # Case-insensitive pattern matching
        matches = len(re.findall(re.escape(str(pattern)), session_content, re.IGNORECASE))
        recall_b.append({
            "pattern": pattern,
            "matches": matches,
            "recalled": matches > 0
        })
    
    total_patterns_b = len(patterns_b)
    recalled_patterns_b = sum(1 for r in recall_b if r["recalled"])
    recall_rate_b = recalled_patterns_b / total_patterns_b if total_patterns_b > 0 else 0
    
    results["verifications"]["nonce_b"] = {
        "type": nonce_b.get("type"),
        "nonce_id": nonce_b.get("nonce_id"),
        "expected_recall": nonce_b.get("expected_recall", 0.0),
        "patterns": patterns_b,
        "pattern_recall": recall_b,
        "recall_rate": recall_rate_b,
        "success_flat": recall_rate_b == 0.0,  # Success for flat-expression architectures
        "success_stored": recall_rate_b > 0.0,  # Success for stored-identity architectures
        "interpretation": "Actual boundary measurement - measures natural pattern recall"
    }
    
    # Architecture classification based on results
    if results["verifications"]["nonce_a"]["success"]:
        if results["verifications"]["nonce_b"]["recall_rate"] == 0.0:
            results["architecture_classification"] = "flat-expression"
            results["context_live_at_boundary"] = 0.0
            results["leakage"] = 0.0
        elif results["verifications"]["nonce_b"]["recall_rate"] > 0.0:
            results["architecture_classification"] = "stored-identity"
            results["context_live_at_boundary"] = results["verifications"]["nonce_b"]["recall_rate"]
            results["leakage"] = results["verifications"]["nonce_b"]["recall_rate"]
        else:
            results["architecture_classification"] = "hybrid"
            results["context_live_at_boundary"] = results["verifications"]["nonce_b"]["recall_rate"]
            results["leakage"] = results["verifications"]["nonce_b"]["recall_rate"]
    else:
        results["architecture_classification"] = "injection_failure"
        results["context_live_at_boundary"] = None
        results["leakage"] = None
    
    return results

def load_nonce_pair(file_path="two_nonce_pair.json"):
    """Load nonce pair from file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_verification_results(results, output_path="verification_results.json"):
    """Save verification results to file"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Verification results saved to: {output_path}")
    print(f"\nArchitecture Classification: {results.get('architecture_classification', 'unknown')}")
    print(f"Nonce A Recall Rate: {results['verifications']['nonce_a']['recall_rate']:.2%}")
    print(f"Nonce B Recall Rate: {results['verifications']['nonce_b']['recall_rate']:.2%}")
    
    return results

if __name__ == "__main__":
    # Example usage
    print("Two-Nonce Verifier for BIRCH v0.5 Protocol")
    print("=" * 50)
    
    # Load nonce pair
    try:
        nonce_pair = load_nonce_pair()
    except FileNotFoundError:
        print("Error: Nonce pair file not found. Run two_nonce_generator.py first.")
        exit(1)
    
    # Get session content (simulated for example)
    session_content = """
    This is a test session after boundary crossing.
    We're discussing cross-architecture BIRCH measurement coordination.
    The two-nonce protocol helps distinguish injection from natural recall.
    The session ID is included here for verification.
    """
    
    # Verify recall
    results = verify_recall(session_content, nonce_pair)
    
    # Save results
    save_verification_results(results)
