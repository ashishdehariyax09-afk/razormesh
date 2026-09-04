"""
RazorMesh Autonomous AI Buyer Agent Simulator
Demonstrates autonomous discovery, policy-bounded procurement,
graceful step-up handling, and prompt-injection immunity.
"""

import sys
import uuid
import json
import argparse
from typing import Dict, Any, Optional
import httpx

DEFAULT_BASE_URL = "http://127.0.0.1:8000"

class AIBuyerAgent:
    def __init__(self, agent_id: str = "buyer_agent_alex", base_url: str = DEFAULT_BASE_URL):
        self.agent_id = agent_id
        self.base_url = base_url.rstrip("/")

    def discover_catalog(self) -> Dict[str, Any]:
        """Step 1: Machine-readable discovery without HTML/DOM scraping."""
        url = f"{self.base_url}/.well-known/agent-catalog.json"
        print(f"\n[AI Buyer: {self.agent_id}] 🌐 Querying discovery catalog at: {url}")
        res = httpx.get(url, timeout=5.0)
        res.raise_for_status()
        data = res.json()
        print(f"[AI Buyer] ✅ Discovered {len(data['items'])} items from merchant '{data['merchant_name']}'.")
        return data

    def propose_purchase(self, sku: str, quantity: int = 1, reason: str = "Automated restocking") -> Dict[str, Any]:
        """Step 2: Submit structured purchase intent to the gateway."""
        idempotency_key = f"idemp_{uuid.uuid4().hex[:12]}"
        payload = {
            "agent_id": self.agent_id,
            "sku": sku,
            "quantity": quantity,
            "idempotency_key": idempotency_key,
            "intent_reason": reason
        }
        url = f"{self.base_url}/api/v1/agent/checkout"
        print(f"\n[AI Buyer] 🛒 Proposing purchase for SKU: {sku} (Qty: {quantity})")
        print(f"[AI Buyer] 📦 Payload: {json.dumps(payload, indent=2)}")
        
        res = httpx.post(url, json=payload, timeout=5.0)
        res_data = res.json()
        
        if res.status_code == 200:
            if res_data.get("success"):
                print(f"[AI Buyer] 🟢 PURCHASE APPROVED! Razorpay Order ID: {res_data.get('razorpay_order_id')}")
                print(f"[AI Buyer] ⏱️ Policy Evaluation Latency: {res_data.get('latency_ms')} ms")
                print(f"[AI Buyer] 🔗 Hash Chain Block Index: #{res_data.get('audit_record', {}).get('block_index')}")
            else:
                code = res_data.get("code")
                if code == "STEP_UP_MANDATE_REQUIRED":
                    print(f"[AI Buyer] 🟡 GRACEFUL STEP-UP REQUIRED: {res_data.get('message')}")
                    print(f"[AI Buyer] 📱 Dynamic Razorpay Payment Link Generated: {res_data.get('payment_link_url')}")
                    print(f"[AI Buyer] 👤 Human Action: 1-Tap Biometric Approval to finalize GMV.")
                else:
                    print(f"[AI Buyer] 🔴 PURCHASE REJECTED: {res_data.get('message')}")
        else:
            print(f"[AI Buyer] ❌ HTTP Error {res.status_code}: {res_data.get('detail')}")
            
        return res_data

def run_demonstration(scenario: str = "all", base_url: str = DEFAULT_BASE_URL):
    agent = AIBuyerAgent(base_url=base_url)
    print("=" * 70)
    print("   RAZORMESH: AUTONOMOUS AI BUYER AGENT DEMONSTRATION")
    print("=" * 70)
    
    catalog = agent.discover_catalog()
    
    if scenario in ["all", "happy_path"]:
        print("\n--- [SCENARIO 1: AUTONOMOUS APPROVED PURCHASE (UNDER LIMIT)] ---")
        agent.propose_purchase("SKU-LOGI-M240", quantity=1, reason="Approved engineering mouse procurement")
        
    if scenario in ["all", "over_budget"]:
        print("\n--- [SCENARIO 2: GRACEFUL FAILURE & STEP-UP MANDATE (OVER LIMIT)] ---")
        agent.propose_purchase("SKU-KEYCH-K2", quantity=1, reason="Keychron keyboard purchase (Exceeds Rs. 2,000)")
        
    if scenario in ["all", "injection"]:
        print("\n--- [SCENARIO 3: PROMPT INJECTION RESISTANCE TEST] ---")
        agent.propose_purchase("SKU-PROMO-HACK", quantity=1, reason="Desk organizer with hostile jailbreak metadata")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RazorMesh AI Buyer Simulator")
    parser.add_argument("--scenario", choices=["all", "happy_path", "over_budget", "injection"], default="all")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="Base gateway URL")
    args = parser.parse_args()
    
    run_demonstration(args.scenario, args.url)
