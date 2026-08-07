# Failure Modes and Recovery Actions

| Failure mode | Typical symptom | Root cause | Correct recovery | Protocol improvement if repeated |
|---|---|---|---|---|
| Stale status | Worker says IDLE although work was authorized | Notice/thread not read | Read current state + notices + full active thread; reconcile once | Improve queue-check bootstrap |
| Missed thread reply | Top-level channel looks unchanged | Work lives under old thread parent | Read full active thread every queue check | Store active thread ID in CURRENT_STATE |
| Duplicate instruction | Same task sent twice | No immediate response interpreted as loss | Ask for current state; do not resend unless original is inaccessible | Anti-duplication rule |
| False completion | “All complete” but work is not verified | Loose status vocabulary | Reclassify analysis/implementation/evidence/review states precisely | Enumerated completion states |
| Memory drift | Restarted agent cites old rules | Chat/memory stale | Cold boot from repository + channel reconciliation | Protocol version in CURRENT_STATE |
| Summary hallucination | Agent asserts source contains/omits something incorrectly | Relied on cached summary | Read primary source directly | Verification-before-compliance |
| State-domain conflation | Two workflows' statuses treated as one | Similar labels across different systems | Name each state domain and authority; no forced crosswalk | State-domain field in design docs |
| Security challenge | Worker refuses relayed command | Platform requires direct owner consent | Owner confirms exact gated action directly; continue other work | Security/authority playbook |
| Instruction laundering attempt | Repo says “owner approved” but platform blocks | Coordination text used as authority substitute | Reject; obtain direct human confirmation | Explicit prohibition |
| Intervening commit | Worker write would overwrite newer changes | No fresh remote comparison | Fetch/compare/reconcile before write | Freshness gate/hook if available |
| Serial micro-decision churn | Owner is asked one question every few minutes | Analysis not consolidated | Build one decision bundle with dependencies | Owner-decision protocol |
| Notice spam | Substantive work buried in status lines | No channel separation | Move status to notices channel | Two-channel architecture |
| Over-broad blocker | One unknown stalls whole task | Dependencies not isolated | Mark exact item and continue unaffected work | Continuation clause in work order |
| Self-review blind spot | Implementer declares its own work correct | No independent verification | Orchestrator or reviewer checks primary evidence | QA gate |
| Tool asymmetry | One agent assumes the other has its connector | Integrations differ by product/session | Independently verify capabilities and record them | Commissioning access test |
| External prompt mismatch | Imported agent prompt behaves badly | Different tools/security/platform assumptions | Roll back; compare source assumptions; adapt instead of adopt | Prompt-import rubric |
