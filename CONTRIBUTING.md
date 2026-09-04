# Contributing to RazorMesh

Thank you for your interest in contributing to **RazorMesh** (Track 01: Autonomous Agentic Commerce — Razorpay AI Buildathon 2026).

## Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ashishdehariyax09-afk/razormesh.git
   cd razormesh
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the 15-Case Adversarial Test Suite**:
   ```bash
   python test_adversarial.py
   ```
   All 15 tests must pass with 0 failures before opening a pull request.

4. **Launch Local Server & Cockpit**:
   ```bash
   python run.py
   ```
   Open `http://127.0.0.1:8000` in your browser.

## Code Standards & Guidelines

- **Zero Breaking Changes**: Preserve existing API contracts (`/.well-known/agent-catalog.json`, `/api/v1/agent/checkout`, `/api/v1/policy`, `/api/v1/audit/integrity`).
- **Deterministic Security First**: Never grant LLMs or external parameters authority over policy gates or pricing calculations.
- **Cryptographic Audit Chain**: Any new transaction state transition must append a block via `audit_engine.append_audit_block()`.
- **Commit Messages**: Follow standard conventional commits (e.g. `feat: ...`, `fix: ...`, `docs: ...`).
