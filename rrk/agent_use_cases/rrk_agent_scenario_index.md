# RRK Agent Scenario Index

## Core Framework

**Clarify → Architecture → Workflow → Failure Modes → Guardrails → Evals → Rollout**

Use this structure for every role-related GenAI agent scenario.

- **Clarify:** user, workflow, systems of record, action boundaries, success metrics
- **Architecture:** UI, orchestrator, retrieval layer, tool layer, decision layer, action layer
- **Workflow:** walk through one concrete user request end-to-end
- **Failure Modes:** what can go wrong and how to mitigate it
- **Guardrails:** add controls mapped to those risks
- **Evals:** offline golden cases + online business metrics
- **Rollout:** read-only assistant → drafting copilot → approved actions → limited autonomy

---

## Simplified Example: Retail Store Operations Copilot

### Problem

A large retailer wants an AI agent for store associates and managers. Associates need help with inventory discrepancies, pickup order substitutions, return-policy questions, promotions, and operational escalations.

Example user question:

> “Pickup order 12345 needs organic strawberries, but the shelf is empty. What should I do?”

### Simplified Solution

I would design this as a **store operations copilot**, not a fully autonomous retail agent on day one.

The agent would combine:

- **RAG** over store policies, return rules, substitution rules, safety procedures, and operations manuals
- **Typed tool calls** into inventory, product catalog, planogram, order, promotion, and escalation systems
- **Deterministic business rules** for crisp decisions like return eligibility, substitution eligibility, approval requirements, and safety escalation
- **Human approval gates** for high-impact actions like refunds, order cancellation, price overrides, and inventory changes

For the strawberry pickup example, the agent would check the order, SKU, inventory, planogram location, backroom location, recent deliveries, customer substitution preference, and substitution policy.

A good answer might be:

> “The system shows 8 units on hand, but that does not guarantee they are on the shelf. First check the backroom produce bin because this SKU was received this morning. If unavailable, the customer allows substitutions, and the approved substitutes are conventional strawberries 1 lb or organic raspberries 6 oz. Manager approval is not required. I can draft the substitution update for your confirmation.”

The structured output could include:

```json
{
  "workflow": "pickup_order_exception",
  "order_id": "12345",
  "sku": "organic_strawberries_1lb",
  "system_on_hand": 8,
  "customer_allows_substitution": true,
  "manager_approval_required": false,
  "can_auto_execute": false,
  "recommended_next_action": "draft_substitution_update"
}
```

### Top Failure Modes

- Inventory says “on hand,” but the item is not actually on the shelf
- Agent uses stale or wrong-region policy
- Associate sees data they are not authorized to access
- Agent executes a refund, cancellation, or inventory change without approval
- Associates lose trust because answers are slow, vague, or unsupported

### Top Guardrails

- Inventory confidence check before promising “on hand” availability
- Region, store, effective-date, and policy-version filters for policy answers
- Permission-aware retrieval so unauthorized data never enters the prompt
- Human approval gates for refunds, cancellations, and inventory changes
- Source-required answers with confidence level and last-updated timestamp
- Typed tools with schema validation, business-rule checks, and safe failure
- Audit logs for retrieved data, proposed actions, approvals, and executed changes
- Manual escalation when evidence is missing, conflicting, stale, or high-risk

### Top Evals

Offline:

- workflow classification accuracy
- policy/decision correctness
- correct tool calls and cited sources

Online:

- time to resolve store issue
- pickup cancellation/substitution error rate
- manager escalation or override rate

### Rollout

1. Read-only policy and lookup assistant
2. Drafting assistant for substitutions, discrepancy reports, and escalations
3. Human-approved tool execution
4. Limited autonomy for low-risk, reversible actions only

---

## Scenario List

| Scenario | File | Status |
|---|---|---|
| Retail Store Operations Copilot | `agent-use-cases/retail-store-operations-copilot.md` | Drafted |
| Warehouse Operations Copilot | `agent-use-cases/warehouse-operations-copilot.md` | Planned |
| Field Technician Copilot | `agent-use-cases/field-technician-copilot.md` | Planned |
| Procurement Agent | `agent-use-cases/procurement-agent.md` | Drafted |
| Customer Support Agent | `agent-use-cases/customer-support-agent.md` | Planned |
| SRE Incident Response Agent | `agent-use-cases/sre-incident-response-agent.md` | Planned |
| RFP / Sales Engineering Agent | `agent-use-cases/rfp-sales-engineering-agent.md` | Planned |
| Legal Contract Review Agent | `agent-use-cases/legal-contract-review-agent.md` | Planned |
| Data Governance Agent | `agent-use-cases/data-governance-agent.md` | Planned |
| Employee Learning Copilot | `agent-use-cases/employee-learning-copilot.md` | Planned |
