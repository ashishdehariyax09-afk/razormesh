"""
RazorMesh Cryptographic Audit Engine
Append-only SHA-256 hash chaining (H_n = SHA256(CanonicalPayload + H_{n-1})).
Guarantees tamper-evident decision history across all transactions.
Supports outer transaction context without nested BEGIN collisions.
"""

import sqlite3
import hashlib
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from database import get_db

GENESIS_PREVIOUS_HASH = "0" * 64

def append_audit_block(
    event_id: str,
    agent_id: str,
    action: str,
    amount_inr: float,
    status: str,
    decision_reason: str,
    conn: Optional[sqlite3.Connection] = None
) -> Dict[str, Any]:
    should_close = False
    if conn is None:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE;")
        should_close = True
    else:
        cursor = conn.cursor()
        
    try:
        cursor.execute("SELECT block_index, current_hash FROM audit_chain ORDER BY block_index DESC LIMIT 1;")
        last_row = cursor.fetchone()
        
        previous_hash = last_row["current_hash"] if last_row else GENESIS_PREVIOUS_HASH
        new_index = (last_row["block_index"] + 1) if last_row else 1
        timestamp = datetime.now(timezone.utc).isoformat()
        
        canonical_payload = f"{event_id}|{timestamp}|{agent_id}|{action}|{amount_inr:.2f}|{status}|{decision_reason}|{previous_hash}"
        current_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
        
        cursor.execute("""
            INSERT INTO audit_chain 
            (block_index, event_id, timestamp, agent_id, action, amount_inr, status, decision_reason, previous_hash, current_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_index, event_id, timestamp, agent_id, action, amount_inr, status, decision_reason, previous_hash, current_hash))
        
        if should_close:
            conn.commit()
            
        return {
            "block_index": new_index,
            "event_id": event_id,
            "timestamp": timestamp,
            "agent_id": agent_id,
            "action": action,
            "amount_inr": amount_inr,
            "status": status,
            "decision_reason": decision_reason,
            "previous_hash": previous_hash,
            "current_hash": current_hash
        }
    finally:
        if should_close:
            conn.close()

def verify_audit_integrity() -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_chain ORDER BY block_index ASC;")
        blocks = cursor.fetchall()
        
        if not blocks:
            return {
                "valid": True,
                "total_blocks": 0,
                "message": "Audit chain is empty (Genesis state)"
            }
            
        expected_previous_hash = GENESIS_PREVIOUS_HASH
        for block in blocks:
            if block["previous_hash"] != expected_previous_hash:
                return {
                    "valid": False,
                    "failed_block_index": block["block_index"],
                    "error": "Previous hash pointer mismatch",
                    "expected": expected_previous_hash,
                    "actual": block["previous_hash"]
                }
                
            payload = f"{block['event_id']}|{block['timestamp']}|{block['agent_id']}|{block['action']}|{block['amount_inr']:.2f}|{block['status']}|{block['decision_reason']}|{block['previous_hash']}"
            recalculated_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            
            if recalculated_hash != block["current_hash"]:
                return {
                    "valid": False,
                    "failed_block_index": block["block_index"],
                    "error": "Payload tampered; hash mismatch",
                    "recalculated": recalculated_hash,
                    "recorded": block["current_hash"]
                }
                
            expected_previous_hash = block["current_hash"]
            
        return {
            "valid": True,
            "total_blocks": len(blocks),
            "latest_block_index": blocks[-1]["block_index"],
            "latest_hash": blocks[-1]["current_hash"],
            "message": "100% Cryptographic Continuity Verified across all audit blocks."
        }

def get_recent_audit_blocks(limit: int = 15) -> List[Dict[str, Any]]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_chain ORDER BY block_index DESC LIMIT ?;", (limit,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

if __name__ == "__main__":
    b = append_audit_block("evt_test", "agent_1", "TEST_ACTION", 10.0, "SUCCESS", "Manual test")
    print("Appended:", b["block_index"], b["current_hash"][:16])
