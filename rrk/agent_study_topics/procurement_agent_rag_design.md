# Production-Grade RAG for a Procurement Agent

## Goal

Design a modern Retrieval-Augmented Generation (RAG) layer that helps a procurement agent answer policy, vendor, contract, approval, and compliance questions using grounded, permission-aware evidence.

The key principle:

> Treat RAG as an evidence orchestration layer, not just vector search.

The LLM should not be expected to “know” procurement policy. It should retrieve current, authorized, source-backed evidence, reason from that evidence, cite it, and abstain or escalate when evidence is incomplete.

---

## Modern RAG Workflow

A production RAG workflow is roughly:

1. Understand the user query and classify the intent.
2. Rewrite or decompose the query if needed.
3. Apply metadata and permission filters before retrieval.
4. Run semantic vector search.
5. Run keyword / lexical search such as BM25.
6. Optionally run multiple searches against different corpora: policy, contracts, vendor docs, approval matrix, security docs, prior tickets.
7. Merge and deduplicate candidate evidence.
8. Rerank the evidence using a stronger reranker or LLM-based relevance step.
9. Expand selected child chunks into parent context when needed.
10. Return evidence with source name, section, page, date, version, authority level, and citation ID.
11. Generate an answer grounded only in supported evidence.
12. Verify whether key claims are actually supported by the evidence.
13. If evidence is missing, stale, conflicting, or unauthorized, ask a follow-up or escalate.

In short:

> Query understanding → hybrid retrieval → metadata filtering → reranking → context assembly → grounded generation → claim verification.

---

## Hybrid Retrieval

Modern RAG usually combines **vector search** and **keyword search**.

### Vector search

Vector search uses embeddings to find text with similar meaning, even when the exact words differ.

Example:

- Query: “Can I buy laptops without approval?”
- Retrieved text: “Hardware purchases under $2,500 do not require manager authorization.”

Vector search is strong for semantic similarity, paraphrases, vague questions, and concept-level matching.

### Keyword search / BM25

Keyword search is better for exact terms:

- policy names
- policy IDs
- contract IDs
- vendor names
- claim numbers
- SKU numbers
- error codes
- legal terms
- acronyms
- section numbers

Example:

- Query: “PROC-HW-US-2026 section 4.2”
- BM25 is likely better than vector search at finding the exact policy and section.

A strong production system usually uses both:

> Vector search finds meaning. BM25 finds exact identifiers. Reranking chooses the best evidence.

---

## Chunking and Context Design

Chunking should preserve logical meaning, not just split by character count.

Good chunk boundaries depend on the source type:

- policies: section, subsection, rule, exception
- contracts: clause, pricing section, renewal clause, termination clause, SLA, liability section
- code: function, class, module
- tickets: issue, resolution, timeline
- tables: row group, table section, caption, footnotes
- PDFs: section title, page number, table/image references

Each chunk should carry useful metadata:

- document title
- source system
- section heading
- page number
- effective date
- expiration date
- document version
- region / jurisdiction
- business unit
- category such as hardware, software, SaaS, services
- authority level such as official policy, draft, email, contract, FAQ
- access-control metadata
- abbreviation explanations when needed

A useful pattern is **child-parent retrieval**:

- Embed a small child chunk for precise semantic retrieval.
- Return a larger parent chunk for richer context.

Example:

Child chunk:

> Purchases under $2,500 do not require manager approval.

Parent chunk:

> This rule applies only to U.S. office hardware purchases from pre-approved vendors. Software and SaaS purchases follow the security-review workflow.

This gives both precision and context.

---

## Evidence Types for Procurement

A procurement RAG layer should not treat all documents equally.

Relevant evidence sources may include:

- procurement policy documents
- approval threshold tables
- regional exceptions
- vendor onboarding rules
- contract repository documents
- DPAs and security-review policies
- finance / budget policies
- preferred vendor lists
- historical procurement tickets
- internal FAQs and playbooks

But some facts should come from **tools and systems of record**, not stale documents.

Examples:

- vendor approval status should come from vendor master
- budget availability should come from finance system
- contract active/expired status should come from contract system
- user permissions should come from IAM
- approval chain should come from approval matrix or workflow system

Rule of thumb:

> Use RAG for unstructured policy and contract interpretation. Use tools for live source-of-record facts.

---

## Production Guardrails

A procurement RAG system needs more than relevant chunks.

Important guardrails:

- Permission-aware retrieval before documents enter the prompt.
- Metadata filters for region, date, policy version, category, and business unit.
- Source-authority ranking so official current policy beats old slides, emails, or drafts.
- Freshness checks for effective date and expiration date.
- Conflict detection when sources disagree.
- Required citations for policy or compliance claims.
- Abstention when evidence is insufficient.
- Clear separation between retrieved evidence and executable action.
- Audit logs showing query, retrieved evidence, model answer, citations, and tool calls.

Important interview phrase:

> Retrieval is not just relevance. In enterprise RAG, retrieval is relevance plus permission, authority, freshness, and applicability.

---

## Hard / Open Problems in RAG

### 1. Multi-hop evidence

Many procurement questions cannot be answered from one chunk.

Example:

> Can an employee in Germany buy this SaaS vendor to process customer data?

This may require combining evidence from:

- regional procurement policy
- vendor approval status
- contract status
- DPA requirements
- security review rules
- approval thresholds
- employee role and cost center

The hard problem is not just retrieving more chunks. The hard problem is knowing whether the system has gathered enough evidence to answer safely.

Key question:

> How does the system know the evidence graph is complete enough to support the decision?

### 2. Global corpus questions / GraphRAG

Some questions are not answered by the nearest chunks.

Examples:

- What are the main procurement bottlenecks across all tickets this quarter?
- Which policies contradict each other across regions?
- Which vendor categories create the most compliance risk?
- What themes appear across thousands of contract exceptions?

These require aggregation, clustering, entity extraction, relationship modeling, and summarization across the corpus.

GraphRAG-style approaches help by representing entities and relationships:

- vendor → contract
- contract → region
- region → policy
- policy → approval threshold
- vendor → security review
- request → cost center

The hard problem is turning a document corpus into a structured evidence graph that can support global and multi-hop questions.

### 3. Faithfulness and claim-level support

A RAG system can retrieve good evidence and still answer incorrectly.

Failure modes:

- answer overgeneralizes beyond the source
- answer misses an exception
- citation is related but does not support the claim
- stale policy is cited as current
- regional rule is applied globally
- model uses prior knowledge instead of retrieved evidence

The hard problem is claim-level verification:

1. Break the answer into claims.
2. Map each claim to supporting evidence.
3. Check whether the evidence supports, contradicts, or is insufficient.
4. Remove or qualify unsupported claims.

Important phrase:

> Citations are not enough. The system must verify that each important claim is actually entailed by the cited evidence.

### 4. Source authority and freshness

Enterprise corpora contain many true-but-wrong documents:

- old policies
- draft policies
- outdated slide decks
- old email attachments
- copied PDFs
- superseded contract terms
- regional exceptions
- unofficial summaries

The most semantically relevant chunk may be operationally wrong.

The hard problem is authority-aware retrieval:

> Which source wins when two relevant sources disagree?

A strong system needs a source hierarchy, such as:

1. IAM / access-control system
2. system of record
3. current official policy
4. active contract
5. approved playbook
6. FAQ / historical ticket
7. email / draft / slide deck

### 5. Evaluation of RAG quality

RAG quality has multiple layers:

- Did retrieval find the right evidence?
- Did reranking choose the right evidence?
- Did the model answer from the evidence?
- Were citations correct?
- Did the system abstain when evidence was missing?
- Did metadata filters avoid stale or unauthorized sources?
- Did the answer lead to the right business decision?

For procurement, evals should include golden test cases:

- approved vendor vs blocked vendor
- U.S. hardware vs EU SaaS
- below-threshold vs above-threshold purchase
- current policy vs expired policy
- conflicting sources
- missing DPA
- unauthorized user
- prompt injection inside retrieved document

---

## Interview-Ready Summary

A strong answer:

> For a procurement agent, I would design RAG as an evidence orchestration layer, not a simple vector lookup. I would parse documents into logical chunks, preserve metadata, enforce access permissions before retrieval, combine vector search with BM25 keyword search, rerank evidence, expand child chunks into parent context, and generate answers only from cited evidence. For live facts such as vendor status, budget, contract state, or approval chain, I would use tools connected to systems of record rather than relying on embedded documents. The hard RAG problems are multi-hop evidence, global corpus questions, claim-level faithfulness, source authority, freshness, and evaluation. In enterprise RAG, the question is not just whether a chunk is relevant; it is whether it is authorized, current, authoritative, applicable, and sufficient to support the answer.
