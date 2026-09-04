# Security Policy

## Overview
RazorMesh is designed as a **Zero-Trust Autonomous Agentic Commerce Gateway**. The system enforces strict separation between non-deterministic AI intent generation and non-reversible financial settlement on Razorpay payment rails.

## Security Architecture & Guarantees

1. **Zero LLM Authority**: Language models generate purchase intent envelopes; they never possess payment authorization credentials. All spending limits, category allowlists, and single transaction ceilings are hardcoded and mathematically enforced via Python database mutex locks.
2. **Authoritative Price Decoupling**: Client-submitted unit prices in JSON payloads are unconditionally ignored. Pricing is strictly calculated from the merchant database catalog.
3. **Cryptographic SHA-256 Ledger Lock**: Every policy decision (allow, step-up, reject) is cryptographically chained via $H_n = \text{SHA256}(\text{CanonicalPayload}_n \parallel H_{n-1})$. Any database tampering results in immediate hash chain invalidation.
4. **Dynamic Step-Up Mandates**: Sub-ceiling transactions ($\le \text{₹}2,000$) execute autonomously. High-value transactions dynamically escalate to 1-tap biometric human authorization via Razorpay Payment Links in accordance with RBI directives.
5. **HMAC Webhook Signature Integrity**: Official Razorpay webhook callbacks are verified using HMAC-SHA256 signature verification.

## Reporting a Vulnerability

If you discover a security vulnerability or potential bypass within RazorMesh:

1. **Do NOT open a public GitHub issue.**
2. Email security details directly to `ashishdehariyax09@gmail.com` with the subject `[SECURITY] RazorMesh Vulnerability Report`.
3. Include reproduction steps, sample payloads, and expected vs actual gateway behavior.
4. Reports are acknowledged within 24 hours and patch updates are committed promptly.
