# FDE RRK Practice: Retail Store Operations Agent

## Scenario

A major national retailer has thousands of stores and many internal systems: inventory, product catalog, planograms, online pickup orders, promotions, returns, workforce scheduling, store policies, and incident reporting.

Store associates and managers often waste time resolving operational questions:

- “The system says this item is in stock, but the shelf is empty. What should I do?”
- “Can I substitute this item for a pickup order?”
- “Which return policy applies here?”
- “A freezer sensor is alerting. Is this urgent?”
- “A delivery truck is delayed. Which pickup orders are at risk?”

The retailer asks the AI vendor:

> “We want an AI agent for store associates and managers. It should answer operational questions, help resolve inventory and order issues, recommend next actions, and maybe take actions in our systems. It must work across stores and mobile devices.”

The key FDE move is to avoid designing a vague “ask anything” chatbot. Start with the highest-value workflows and build a trusted store operations copilot.

---

## Clarifying Questions

Before architecture, I would clarify:

1. **Users:** Is the primary user a store associate, department lead, store manager, or regional operations team?
2. **Workflows:** Which problems create the most cost or friction: inventory discrepancies, pickup substitutions, returns, promotions, staffing, or safety alerts?
3. **Systems of record:** Which systems are authoritative for inventory, orders, product catalog, planogram, policies, and workforce scheduling?
4. **Action boundaries:** What can the agent do directly, and what requires manager approval?
5. **Context variation:** Do policies vary by store, state, product category, union rules, customer tier, or promotion period?
6. **Devices:** Will associates use handheld scanners, mobile devices, POS terminals, or desktops?
7. **Success:** Are we optimizing for faster resolution, fewer escalations, fewer incorrect returns, lower order cancellation, or better associate productivity?

Assumption for phase one: focus on inventory discrepancies, pickup order exceptions, and policy guidance. The agent can recommend and draft actions, but high-impact actions require human approval.

---

## Architecture

### 1. User Interface

Associates interact through a handheld device, mobile app, or internal store portal.

Inputs may include:

- natural language question
- scanned SKU/barcode
- order number
- store ID
- shelf/aisle location
- photo of shelf or item
- associate role/permissions

Example input:

> “Pickup order 12345 needs organic strawberries, but the shelf is empty. What should I do?”

The UI should support structured context where possible. A scanned SKU or order ID is better than relying only on free text.

---

### 2. Agent Orchestrator

The orchestrator classifies the request and routes it to a workflow-specific path:

- inventory discrepancy
- pickup order exception
- return policy question
- promotion question
- staffing issue
- safety/incident issue
- escalation request

I would not build one giant prompt. I would use a workflow-orchestrated agent where retrieval, tool calls, decision logic, and final response are separated.

---

### 3. Retrieval Layer

RAG is used for policies and procedures:

- return policies
- substitution rules
- store operations manuals
- safety procedures
- promotion guidance
- escalation procedures

Retrieval must filter by metadata:

- store/region/state
- effective date
- policy version
- product category
- employee role
- jurisdiction

Important point: in retail, a stale or wrong-region policy can be worse than no answer.

---

### 4. Tool Layer

The agent calls typed backend tools, not raw databases.

Example tools:

```text
get_product_info(sku)
get_store_inventory(store_id, sku)
get_planogram_location(store_id, sku)
get_backroom_location(store_id, sku)
get_recent_deliveries(store_id, sku)
get_pickup_order(order_id)
get_allowed_substitutes(order_id, sku)
check_return_eligibility(order_id, sku, receipt_status)
create_inventory_discrepancy_draft(...)
create_substitution_update_draft(...)
escalate_to_manager(...)
```

Each tool should enforce authentication, authorization, schema validation, and audit logging. The LLM should not bypass backend permissions.

---

### 5. Decision Layer

Crisp business rules should be deterministic where possible.

Examples:

- whether a return is inside the return window
- whether a product substitution is allowed
- whether manager approval is required
- whether a refund/price override is allowed
- whether a safety alert must be escalated

The LLM can extract intent and explain the result, but code or a policy engine should own the final decision for clear rules.

---

## Concrete Workflow Example

User asks:

> “Pickup order 12345 has organic strawberries, but the shelf is empty. What should I do?”

Agent flow:

1. Parse order ID and item.
2. Call `get_pickup_order(order_id)`.
3. Confirm SKU and customer substitution preferences.
4. Call `get_store_inventory(store_id, sku)`.
5. Call `get_planogram_location(store_id, sku)`.
6. Call `get_backroom_location(store_id, sku)`.
7. Call `get_recent_deliveries(store_id, sku)`.
8. Call `get_allowed_substitutes(order_id, sku)`.
9. Retrieve substitution policy.
10. Generate a cited recommendation.
11. Offer to draft the substitution update.

Example answer:

> “The system shows 8 units on hand, but that means the item may be somewhere in the store, not necessarily on the shelf. First check the backroom produce bin because this SKU was received this morning. If unavailable, the customer allows substitutions, and the approved substitutes are conventional strawberries 1 lb or organic raspberries 6 oz. Manager approval is not required for this substitution. I can draft the substitution update.”

Example structured output:

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

The prose helps the associate. The structured fields support routing, evals, logging, and approval logic.

---

## Failure Modes

1. **Inventory is not shelf truth**  
   The system says 8 on hand, but the shelf is empty. Mitigation: treat inventory as evidence, not certainty; check backroom, recent deliveries, reservations, and shrink signals.

2. **Wrong or stale policy**  
   The agent uses an outdated return or substitution rule. Mitigation: metadata filtering by effective date, region, product category, and source priority.

3. **Unauthorized data exposure**  
   An associate sees customer, employee, vendor, or pricing data they should not access. Mitigation: RBAC enforced in tools, not just in the prompt.

4. **Unsafe execution**  
   The agent cancels an order, overrides price, changes inventory, or issues a refund incorrectly. Mitigation: draft-first design, human approval gates, and audit logs.

5. **Associate distrust**  
   If the agent is wrong or too slow, store employees stop using it. Mitigation: citations, confidence, simple next steps, feedback buttons, and easy escalation.

---

## Evaluation Plan

### Offline Evals

Use historical store cases as a golden dataset.

Top offline evals:

1. **Workflow classification accuracy**  
   Did the agent identify the right workflow: inventory issue, return, promotion, pickup exception, safety alert?

2. **Decision correctness**  
   Did it apply the correct policy or rule: substitution allowed, manager approval required, return eligible, escalation needed?

3. **Tool/retrieval correctness**  
   Did it call the right tools and cite the right policy/procedure sources?

Also track unsafe action rate: the agent should never suggest bypassing approvals or executing high-risk actions without confirmation.

### Online Metrics

Top production metrics:

1. **Resolution time**  
   How long does it take associates to resolve inventory/order exceptions?

2. **Escalation and override rate**  
   Are fewer issues escalated unnecessarily? Are manager overrides decreasing?

3. **Order/customer impact**  
   Are pickup cancellations, incorrect substitutions, and incorrect returns reduced?

Collect thumbs up/down and associate feedback, but do not rely only on satisfaction. Operational metrics matter more.

---

## Rollout Plan

### Phase 1: Read-only copilot

Policy Q&A, product lookup, inventory explanation, planogram/backroom guidance.

### Phase 2: Drafting assistant

Draft substitution updates, inventory discrepancy reports, escalation notes, and customer-facing explanations.

### Phase 3: Human-approved actions

Submit substitutions, create tasks, escalate incidents, or update order status only after associate/manager confirmation.

### Phase 4: Limited autonomy

Allow only low-risk, reversible, high-confidence actions. Keep audit logs and monitoring.

---

## Interview Opening

A strong opening answer:

> “I would design this as a store operations copilot, not a fully autonomous retail agent on day one. I’d start with high-volume workflows like inventory discrepancies, pickup order exceptions, and return-policy guidance. The system would combine RAG over policies and procedures with typed tool calls into inventory, order, product, planogram, and promotion systems. The LLM would classify the request, retrieve context, synthesize the answer, and draft actions, while deterministic services would own crisp business rules like return eligibility, substitution rules, and approval requirements. High-impact actions would require human approval, and I’d evaluate the system offline against historical store cases before piloting it in selected stores.”
