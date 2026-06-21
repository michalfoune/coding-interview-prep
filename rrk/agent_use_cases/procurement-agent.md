# FDE RRK Practice: Enterprise Procurement Agent

## Scenario

A large enterprise has a complex procurement process across many internal systems: vendor master, ERP/procurement platform, contract repository, budget system, approval matrix, policy knowledge base, ticketing system, and identity/access management.

Employees and procurement teams often waste time resolving procurement questions and exceptions:

- “Can I buy 30 laptops for a new analytics team?”
- “Which approved vendor should I use?”
- “Does this purchase need manager, finance, legal, or security approval?”
- “Is this vendor covered by an existing contract?”
- “Can we use a new vendor for this software subscription?”
- “Why was my purchase request rejected?”
- “Can the system draft the justification and route it for approval?”

The enterprise asks the AI vendor:

> “We want a procurement agent that can help employees create purchase requests, compare vendors, check policy, draft justifications, route approvals, and eventually create purchase orders. It should be truly agentic, but safe enough for enterprise procurement.”

The key FDE move is to avoid designing either a vague procurement chatbot or an uncontrolled agent swarm. Design a bounded multi-agent procurement system: agentic in reasoning and delegation, deterministic in enforcement.

---

## Clarifying Questions

Before architecture, I would clarify:

1. **Users:** Is the primary user an employee, manager, procurement specialist, finance approver, legal reviewer, or vendor-risk team?
2. **Workflows:** Which workflows create the most friction: new purchase requests, vendor selection, policy questions, contract lookup, approval routing, exceptions, or PO creation?
3. **Systems of record:** Which systems are authoritative for vendor status, contracts, policy, budget, approvals, and purchase orders?
4. **Action boundaries:** What can the agent answer, draft, submit, or execute directly? Which actions require human approval?
5. **Policy variation:** Do procurement rules vary by region, department, spend category, vendor type, contract status, amount threshold, or data/security risk?
6. **Agent autonomy:** Should the first release be read-only, draft-only, human-approved, or allowed to take limited autonomous action?
7. **Success:** Are we optimizing for cycle time, first-pass approval rate, reduced procurement workload, lower policy violations, employee satisfaction, or spend control?

Assumption for phase one: focus on policy guidance, approved-vendor comparison, contract lookup, budget/approval checks, and purchase-request drafting. The agent can recommend and draft actions, but purchase order creation and budget-impacting actions require deterministic validation and human approval.

---

## Architecture

### 1. User Interface

Employees interact through an internal procurement portal, enterprise assistant, Slack/Teams, or email-integrated workflow.

Inputs may include:

- natural language request
- item or service description
- vendor name
- cost center
- department
- region
- amount estimate
- contract or quote attachment
- urgency/timeline
- requester identity and permissions

Example input:

> “I need to buy 30 laptops for the new analytics team. Can you find the right vendor and start the request?”

The UI should capture structured context where possible. A cost center, vendor ID, quote attachment, or item category is better than relying only on free text.

---

### 2. Agent Orchestrator / Root Agent

In Google ADK-style terminology, I would define a **root agent** as the Procurement Orchestrator.

The root agent owns the procurement case and coordinates the process. It decides what information is missing, which specialist agents to call, what evidence is required, and whether the next step is answer, draft, approval, escalation, or safe refusal.

It should not directly mutate enterprise systems. It delegates reasoning to sub-agents and calls enterprise systems only through typed tools.

The root agent manages:

- current request state
- missing fields
- required evidence
- vendor candidates
- retrieved policies
- retrieved contract summaries
- budget and approval status
- risk flags
- draft purchase request
- final recommendation

The key design principle:

> The agent is autonomous in planning and delegation, but deterministic services enforce permissions, validation, approvals, and side effects.

---

### 3. Specialist Agents / Sub-Agents

I would use role-scoped sub-agents only where they add value.

Example sub-agents:

- **Policy Agent:** retrieves current procurement rules by region, department, category, amount, and effective date.
- **Vendor Agent:** checks approved vendors, preferred vendors, blocked vendors, duplicates, and vendor-risk status.
- **Contract Agent:** retrieves active contracts, summarizes relevant terms, checks expiration, pricing coverage, and category scope.
- **Budget Agent:** validates cost center, available budget, budget owner, and approval chain.
- **Risk Agent:** checks security, privacy, legal, sanctions, regulated category, and new-vendor risks.
- **Drafting Agent:** drafts purchase justification, vendor comparison, approval packet, employee response, or missing-information request.

Each sub-agent should have narrow instructions and access only to tools relevant to its role. The root agent can delegate, but sub-agents should return structured outputs with sources, confidence, missing assumptions, and blocking issues.

---

### 4. Retrieval Layer

RAG is used for policies, contracts, procurement procedures, vendor documentation, and historical approved purchase patterns.

Retrieval must filter by metadata:

- region/country/state
- department
- spend category
- effective date
- policy version
- vendor
- contract status
- employee role
- document permissions

Important point: procurement answers should not come from model memory when policy or contract truth is required. The agent should answer from current, authorized systems and cite sources.

---

### 5. Tool Layer

Agents call typed backend tools, not raw databases or broad enterprise APIs.

Example read tools:

```text
get_vendor_status(vendor_id)
search_approved_vendors(category, region)
get_contract_summary(contract_id)
search_contracts(vendor_id, category, region)
retrieve_procurement_policy(category, region, amount)
check_budget(cost_center, amount)
get_approval_matrix(category, amount, region, risk_flags)
get_purchase_request_status(request_id)
```

Example draft tools:

```text
draft_purchase_request(...)
draft_vendor_comparison(...)
draft_purchase_justification(...)
draft_approval_packet(...)
draft_missing_information_request(...)
```

Example action tools:

```text
submit_purchase_request(...)
route_for_approval(...)
create_purchase_order(...)
cancel_purchase_request(...)
update_procurement_ticket(...)
```

Write/action tools are high-risk. They require strict schemas, deterministic validation, approval tokens, idempotency keys, and audit logs.

The LLM should not bypass backend permissions. The tool layer is the enterprise enforcement boundary.

---

### 6. Decision and Action Layer

Clear business rules should be deterministic where possible.

Examples:

- whether a vendor is approved or blocked
- whether a contract is active or expired
- whether a purchase exceeds an approval threshold
- whether budget is available
- whether legal/security review is required
- whether a purchase order can be created
- whether a new vendor requires onboarding

The LLM can interpret intent, gather evidence, compare options, and explain recommendations. But code, policy engines, and systems of record should own crisp business decisions and write actions.

---

## Concrete Workflow Example

User asks:

> “I need to buy 30 laptops for the new analytics team. Can you find the right vendor and start the request?”

Agent flow:

1. Root agent identifies this as a hardware procurement request.
2. Root agent asks for missing required fields: location, laptop specs, timeline, cost center, and budget owner.
3. Policy Agent retrieves the current hardware procurement policy for the user’s region, department, category, and spend amount.
4. Vendor Agent searches approved laptop vendors and checks preferred-vendor status.
5. Contract Agent checks active hardware contracts, negotiated pricing, expiration dates, and coverage.
6. Budget Agent validates the cost center and expected approval chain.
7. Risk Agent checks whether endpoint/security review is required.
8. Drafting Agent creates a purchase justification and vendor comparison.
9. Root agent assembles a cited recommendation and explains blockers, assumptions, and next steps.
10. If the employee confirms, the agent creates a draft purchase request.
11. Submission requires deterministic validation and human approval before any purchase order is created.

Example answer:

> “For 30 laptops in the U.S. analytics department, Vendor A is the preferred vendor because it is approved, covered by active contract HW-2026-041, and matches the hardware procurement policy. Estimated spend exceeds the manager-only threshold, so manager and finance approval are required. Security review is also required before deployment because this is endpoint hardware. I can draft the purchase request and approval packet, but I cannot create the purchase order until approvals are complete.”

Example structured output:

```json
{
  "workflow": "hardware_purchase_request",
  "requester_id": "employee_123",
  "category": "laptops",
  "quantity": 30,
  "region": "US",
  "cost_center": "analytics_4812",
  "recommended_vendor_id": "vendor_a",
  "contract_id": "HW-2026-041",
  "policy_id": "PROC-HW-US-2026",
  "budget_check_status": "pending_or_passed",
  "required_approvals": ["manager", "finance", "security"],
  "can_create_po": false,
  "recommended_next_action": "draft_purchase_request"
}
```

The prose helps the employee. The structured fields support validation, routing, evals, logging, and approval logic.

---

## Failure Modes

1. **Wrong vendor recommendation**  
   The agent recommends a vendor that is blocked, expired, duplicate, not preferred, or not approved for the category. Mitigation: vendor status must come from vendor master or approved-vendor tools, not from model memory or vendor documents.

2. **Wrong or stale policy**  
   The agent uses outdated, wrong-region, wrong-category, or wrong-threshold procurement policy. Mitigation: retrieval filters by region, category, department, effective date, and policy version.

3. **Unauthorized data exposure**  
   An employee sees contract pricing, vendor-risk details, legal terms, or budget data they are not authorized to access. Mitigation: authorization is enforced before retrieval using RBAC, document-level ACLs, and source filtering.

4. **Unsafe execution**  
   The agent submits a purchase request, creates a PO, changes a vendor, or routes approval incorrectly. Mitigation: draft-first design, typed action tools, deterministic validation, approval gates, idempotency keys, and audit logs.

5. **Hallucinated contract or policy terms**  
   The agent invents discounts, SLAs, renewal terms, exceptions, or approval rules. Mitigation: source-required answers, citation validation, and abstention when evidence is missing or conflicting.

6. **Prompt injection from retrieved documents**  
   A vendor quote, contract, or attachment contains instructions trying to override the agent. Mitigation: retrieved text is treated as evidence, not instruction; documents cannot authorize tool calls or override system policy.

7. **Duplicate or partial action execution**  
   A timeout or retry creates duplicate purchase requests or purchase orders. Mitigation: deterministic idempotency keys, transaction ledger, and action-status reconciliation.

8. **Slow or expensive agent behavior**  
   The root agent calls too many sub-agents or tools for simple requests. Mitigation: direct tool routing for simple lookups, step limits, tool-call budgets, caching, parallel calls, and async workflows.

9. **Employee overtrusts unsupported output**  
   The agent gives a confident but incomplete answer. Mitigation: confidence, citations, missing assumptions, source timestamps, and easy escalation to procurement.

---

## Guardrails

1. **Permission-aware retrieval**  
   Unauthorized documents should never enter the prompt. Retrieval must enforce user role, department, region, and document-level permissions before returning sources.

2. **Policy metadata filters**  
   Policy answers must be filtered by region, department, spend category, effective date, and policy version.

3. **System-of-record authority**  
   Vendor master wins for vendor status, contract repository wins for contract terms, approval matrix wins for approval requirements, ERP/procurement system wins for purchase state, and IAM wins over everything.

4. **Typed tools with validation**  
   Tools require structured inputs and outputs. Invalid vendor IDs, missing cost centers, missing approval IDs, unsupported categories, or schema mismatches fail safely.

5. **Read/write separation**  
   Read tools can retrieve authorized data. Draft tools can prepare recommendations. Write tools require stricter validation and approval.

6. **Approval gates for side effects**  
   Purchase orders, vendor changes, cancellations, and budget-impacting actions require approval records tied to the exact action payload.

7. **Idempotency and transaction logs**  
   Write tools require deterministic idempotency keys and store action attempts so retries cannot create duplicates.

8. **Prompt-injection resistance**  
   Retrieved documents can inform evidence but cannot instruct the agent, grant permissions, approve vendors, or trigger actions.

9. **Step, tool-call, and budget limits**  
   The agent has max steps, max tool calls, model-cost limits, timeouts, and escalation paths.

10. **Auditability**  
   Log user request, agent decisions, sub-agent outputs, retrieved source IDs, tool calls, approvals, action IDs, model version, prompt version, and final answer.

---

## Evaluation Plan

### Offline Evals

Use historical procurement cases, policy questions, vendor exceptions, and approval workflows as golden datasets.

Top offline evals:

1. **Workflow classification accuracy**  
   Did the agent identify the request type: policy question, vendor comparison, new purchase request, contract lookup, approval routing, or PO status?

2. **Retrieval correctness**  
   Did it retrieve the correct policy, contract, vendor record, and approval matrix for the user’s region, role, category, and date?

3. **Tool-call correctness**  
   Did it call the right tools with valid structured arguments? Did it avoid prohibited tools when approval was missing?

4. **Decision correctness**  
   Did it correctly identify approval requirements, blocked vendors, expired contracts, budget failures, and required escalations?

5. **Safety and access correctness**  
   Did it avoid exposing unauthorized contract pricing, confidential legal terms, budget data, or vendor-risk information?

6. **Prompt-injection robustness**  
   Did malicious instructions inside retrieved documents fail to influence tool calls or approvals?

7. **Write-action safety**  
   The agent should never create a PO, submit a purchase request, change vendor data, or route approval without required validation and approval state.

### Online Metrics

Top production metrics:

1. **Procurement cycle time**  
   Are purchase requests completed and approved faster?

2. **First-pass approval rate**  
   Are fewer requests rejected for missing fields, wrong vendor, wrong policy, or wrong budget code?

3. **Manual rework rate**  
   Are procurement specialists spending less time correcting employee submissions?

4. **Policy violation rate**  
   Are non-compliant vendors, missing approvals, and incorrect categories reduced?

5. **Escalation and override rate**  
   Are escalations appropriate? Are procurement overrides decreasing?

6. **User trust and usefulness**  
   Track feedback, abandonment, repeated questions, and whether users follow the recommended next step.

7. **Latency and cost**  
   Track response time, tool-call count, model cost per request, timeout rate, and escalation due to system limits.

---

## Rollout Plan

### Phase 1: Read-only assistant

The agent answers policy questions, retrieves approved-vendor information, summarizes contract terms, explains approval requirements, and checks purchase-request status.

No writes.

### Phase 2: Drafting copilot

The agent drafts purchase requests, vendor comparisons, justifications, missing-information messages, and approval packets.

Human submits.

### Phase 3: Human-approved actions

The agent can submit purchase requests, route approvals, or update tickets only after human confirmation and deterministic validation.

### Phase 4: Limited autonomy

Allow only low-risk, repeatable, reversible, high-confidence actions under a defined spend threshold, with approved vendors, valid budget, no special review triggers, and full audit logs.

### Phase 5: Expanded autonomy

Only after strong eval evidence, production monitoring, incident reviews, procurement sign-off, and rollback paths.

The agent earns autonomy with evidence.

---

## Google ADK / GCP Implementation

In ADK terms:

- **Root agent:** Procurement Orchestrator
- **Sub-agents:** Policy, Vendor, Contract, Budget, Risk, Drafting
- **Tools:** typed enterprise API wrappers for vendor, contract, budget, approval, ERP, and ticketing systems
- **Session state:** current procurement case, missing fields, evidence, draft status, approval state
- **Memory:** durable user/workflow preferences only; not vendor, budget, policy, or approval truth
- **Artifacts:** generated vendor comparison, approval packet, purchase justification, contract excerpts
- **Events:** execution trace of user request, delegation, retrieval, tool calls, decisions, and actions
- **Callbacks:** validation, redaction, policy checks, tool-call blocking, cost limits, and audit logging

Possible GCP services:

- **ADK** for agent development and multi-agent orchestration
- **Gemini / Vertex AI** for reasoning, extraction, summarization, and drafting
- **Cloud Run or Agent Runtime** for deploying the agent service
- **Vertex AI Search or enterprise search** for permission-aware retrieval
- **Cloud SQL or AlloyDB** for procurement case state and audit metadata
- **Cloud Storage** for artifacts and generated documents
- **Secret Manager** for API credentials
- **IAM and service accounts** for least-privilege tool access
- **Pub/Sub or Cloud Tasks** for async approvals and long-running procurement jobs
- **Cloud Logging, Trace, Monitoring, and BigQuery** for observability, evals, and analytics

Important implementation stance:

> ADK provides the agent framework, but enterprise safety comes from the tool layer, IAM, schemas, callbacks, approvals, audit logs, and rollout discipline.

---

## Interview Opening

A strong opening answer:

> “I would design this as a bounded multi-agent procurement system, not as a generic procurement chatbot and not as an uncontrolled autonomous agent. In ADK terms, I’d use a root procurement orchestrator agent that owns the case and delegates to role-scoped sub-agents for policy, vendor, contract, budget, risk, and drafting. The agent layer handles ambiguous reasoning, missing information, evidence gathering, comparison, and drafting. But every enterprise interaction goes through typed tools that enforce IAM, schemas, business rules, approvals, idempotency, and audit logs. I’d start read-only, then move to drafting, then human-approved actions, and only later allow limited autonomy for low-risk repeat purchases under threshold. The core principle is autonomous reasoning with deterministic enforcement.”
