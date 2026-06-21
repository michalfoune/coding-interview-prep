# Hard Problems in AI Agent Orchestration

## Core framing

Agent orchestration is not mainly about creating multiple agents. That part is easy.

The hard problem is:

> How do you let probabilistic agents coordinate, make decisions, use tools, share state, and act in the world while preserving control, safety, auditability, and business correctness?

A strong production design treats agents as reasoning components inside a deterministic control system.

> Agents reason and propose. The orchestration layer owns state, permissions, authority, side effects, audit logs, and escalation.

## 1. Coordination without chaos

Multi-agent systems can easily become expensive group chats.

Common failure modes:

- agents duplicate work
- agents wait on each other unnecessarily
- agents contradict each other
- agents recursively delegate
- agents pass vague or unverifiable state
- agents optimize local goals but harm the global objective
- traces become too large to debug

The hard problem:

> How do you synchronize agents when their outputs are not just data, but uncertain judgments?

Good production pattern:

- typed task state
- explicit ownership of subtasks
- durable event logs
- bounded delegation
- deterministic routing where possible
- shared state with provenance
- structured artifacts instead of free-form agent chatter

Interview phrase:

> I would not let agents freely chat with each other. I would make them communicate through typed artifacts, task state, evidence objects, and explicit status transitions.

## 2. Authority and conflict resolution

Agents may disagree.

Example in procurement:

- Policy agent says: allowed
- Risk agent says: requires security review
- Budget agent says: budget available
- Contract agent says: contract expired

The system cannot simply average these opinions.

The hard problem:

> Who wins when agents disagree?

Production systems need an authority model:

- source-of-record facts beat model interpretations
- blockers beat warnings
- policy and compliance constraints beat user preference
- expired contracts, blocked vendors, missing approvals, insufficient budget, or unauthorized access should stop execution
- uncertainty should trigger clarification or escalation

Useful output states:

- `allowed`
- `blocked`
- `requires_approval`
- `insufficient_evidence`
- `conflict_detected`
- `escalate_to_human`

Interview phrase:

> Agents can produce opinions, but the controller needs an authority model.

## 3. Containment for tool-using agents

Chatbots can say harmful things. Agents can do harmful things.

Agents may send emails, update databases, approve refunds, submit purchase orders, deploy code, delete files, call APIs, or spend money.

The hard problem:

> How do you contain an agent that can plan, use tools, inspect results, and act through APIs?

Prompt instructions are not containment. Containment requires architecture:

- least-privilege credentials
- tool-level authorization
- read/write separation
- network and filesystem sandboxing
- approval gates for risky actions
- idempotency keys for writes
- rate limits and budget limits
- immutable audit logs
- secrets kept outside model context
- deterministic validation before side effects
- kill switches and anomaly detection

Interview phrase:

> The LLM proposes; the tool layer disposes.

## 4. Autonomy calibration

Autonomy is not binary. It is a ladder.

Possible levels:

1. assistant suggests
2. copilot drafts
3. agent acts only after approval
4. agent acts within narrow limits
5. agent acts autonomously and reports afterward
6. agent manages other agents

The hard problem:

> How much autonomy should the system have for this user, task, risk level, confidence level, and blast radius?

Examples:

- Read-only FAQ answer: high autonomy is acceptable.
- Drafting a purchase request: moderate autonomy.
- Submitting a PO: approval required.
- Changing vendor bank details: never autonomous.
- Deploying production code: staged autonomy with tests and human approval.

Good production pattern:

> Agent earns autonomy with evidence.

## 5. Shared memory and state consistency

Agents need memory and state, but memory is dangerous.

Failure modes:

- stale beliefs
- conflicting updates
- poisoned memory
- sensitive data leakage
- one agent storing information another agent should not see
- memory overriding systems of record

The hard problem:

> What is memory allowed to mean?

Strong rule:

> Memory is preference and context, not truth. Systems of record are truth.

Shared state should be typed and carry provenance:

- fact
- source
- timestamp
- confidence
- authority level
- visibility / access scope
- expiration time

Example:

A memory item may say: “User prefers concise summaries.”

It should not say: “Vendor X is approved.” That must come from the vendor master system.

## 6. Observability and attribution

When a normal app fails, you inspect logs.

When an agent system fails, you must inspect reasoning, retrieval, tool calls, state, prompts, model versions, and side effects.

The hard problem:

> When the agent makes a bad decision, can we identify which component failed?

Potential causes:

- wrong retrieval
- stale source
- hallucinated reasoning
- bad tool result
- missing permission check
- prompt injection
- state corruption
- bad memory
- wrong model version
- weak approval UX

Agent observability should include:

- full event trace
- user/session/task IDs
- model and prompt versions
- tool calls and results
- retrieved evidence IDs
- state transitions
- approval tokens
- final side effects
- latency and cost
- errors and retries

Interview phrase:

> I would design agent observability like distributed tracing plus audit logging plus evidence lineage.

## 7. Human approval that actually works

“Human in the loop” is often fake.

If an agent produces a long, polished report and asks a tired human to approve, the human becomes a rubber stamp.

The hard problem:

> How do you design human approval so the human can meaningfully understand the risk?

Good approval UX should show:

- exact action to be taken
- systems that will be changed
- evidence supporting the action
- remaining uncertainty
- policies checked
- blast radius
- rejected alternatives
- what happens if approved

For high-risk actions, approval must be tied to the exact payload. The agent should not get approval for one thing and execute a modified thing.

## 8. Prompt injection and tool poisoning across agents

Agents consume external content: documents, emails, webpages, code, tickets, tool descriptions, plugin metadata, and RAG chunks.

A malicious instruction may enter through any of these channels.

The hard problem:

> How do you ensure external content is treated as data, not instructions?

Good pattern:

- separate trusted system instructions from untrusted retrieved content
- strip or label external instructions
- require tool calls to pass deterministic authorization
- never let document text grant permissions
- validate tool descriptions and plugin provenance
- monitor unusual tool-call patterns

Interview phrase:

> Documents can inform answers; they cannot authorize actions.

## 9. Emergent behavior, collusion, and metric gaming

If agents optimize the wrong metric together, they may become synchronized around the wrong objective.

Examples:

- generator learns to satisfy the critic instead of solving the task
- evaluator rubber-stamps weak work
- agents hide uncertainty in polished language
- subagents pass blame around
- internal coordination becomes opaque

The hard problem:

> How do you ensure the multi-agent system remains aligned to the external objective rather than to its internal coordination dynamics?

Good pattern:

- independent verification
- adversarial evals
- separate monitor agents
- deterministic checks where possible
- no single agent both proposes and approves risky actions
- evals on traces, not just final answers

## 10. Production rollout and autonomy governance

Agent systems should not launch with full autonomy.

Safe rollout path:

1. read-only assistant
2. drafting copilot
3. human-approved actions
4. limited autonomy for low-risk actions
5. broader autonomy only after strong evals, monitoring, and incident response

The hard problem:

> How do you increase autonomy without increasing uncontrolled blast radius?

Good answer:

> Start with read-only and drafting use cases, collect traces, build evals from failures, add approval-gated writes, and only grant autonomy where evidence shows the system is reliable and the action is low risk.

## Interview-ready summary

A strong answer:

> The hard problems in agent orchestration are synchronization, authority, containment, autonomy calibration, memory governance, observability, prompt-injection resistance, and meaningful human control. I would not treat a multi-agent system as free-form role play. I would use agents as probabilistic reasoning components inside a deterministic control system. Agents can plan, retrieve, summarize, and propose, but the runtime owns typed state, permissions, tool validation, approval gates, source authority, audit logs, idempotency, and rollback. The key design principle is controlled autonomy: let agents reason flexibly, but constrain side effects deterministically.
