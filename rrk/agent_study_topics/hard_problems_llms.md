# Hard Problems in Large Language Models

## Core framing

Large language models are no longer just text-completion systems. Modern frontier systems combine pretrained models, post-training, reasoning-time compute, tool use, routing, retrieval, memory, multimodal inputs, and safety layers.

The hard problems are not only “make the model bigger.” They are about capability, reliability, efficiency, controllability, evaluation, and deployment.

> Frontier LLM work is about moving the capability-cost-reliability frontier.

## 1. Reasoning reliability

LLMs can produce impressive reasoning, but they are still inconsistent.

They may solve a hard problem once and fail a similar one later. They may produce plausible but invalid chains of reasoning. They may overfit to familiar patterns, miss edge cases, or confidently answer when the correct move is to abstain.

The hard problem:

> How do we make reasoning reliable, not just impressive on selected examples?

Important directions:

- test-time compute / thinking budgets
- self-consistency and multi-sample reasoning
- verifiers and reward models
- tool-assisted reasoning
- formal checks where possible
- reasoning traces that are useful for debugging without overtrusting them

Interview phrase:

> The frontier is not just models that can reason; it is models that know when their reasoning is reliable enough to act on.

## 2. Query difficulty classification and routing

Not every query deserves the same model, context, or reasoning budget.

A simple factual query should not use the same path as a hard coding task, legal analysis, or multi-hop enterprise workflow.

The hard problem:

> How does the system know how hard the query is before solving it?

Modern systems increasingly route across:

- fast model vs deep reasoning model
- no retrieval vs RAG
- no tools vs tools
- short answer vs planning loop
- low autonomy vs approval-gated action
- cheap path vs expensive path

Failure modes:

- easy queries routed to expensive models
- hard queries routed to weak models
- risky queries treated as harmless
- insufficient retrieval or tool use
- overconfident direct answers

Interview phrase:

> Query routing is hard because the system must estimate difficulty, risk, and required evidence before it has solved the task.

## 3. Hallucination and epistemic calibration

LLMs are optimized to produce plausible continuations, not inherently to know what is true.

They can hallucinate facts, citations, APIs, package names, legal rules, or business policies.

The hard problem:

> How do we make models represent uncertainty honestly and distinguish known, inferred, retrieved, and unknown information?

Important directions:

- retrieval grounding
- source-required answers
- calibrated confidence
- abstention behavior
- verifier models
- claim-level support checks
- separating model memory from source-of-record facts

Production principle:

> For enterprise facts, the model should not be the source of truth. It should reason over sources of truth.

## 4. Long-context reliability

Modern models can accept very long contexts, sometimes hundreds of thousands or millions of tokens.

But long context does not guarantee faithful use of context.

Failure modes:

- missing a key fact buried in the middle
- over-weighting recent or repeated text
- confusing similar documents
- failing to respect document hierarchy
- treating stale or irrelevant text as authoritative
- losing track of constraints across a long prompt

The hard problem:

> How do we make models reliably use the right parts of long context instead of merely accepting long input?

Important directions:

- better attention mechanisms
- context caching
- retrieval plus long context
- structured context assembly
- source metadata
- context compression
- hierarchical summarization
- evidence selection before generation

Interview phrase:

> Long context reduces the need for retrieval in some cases, but it does not eliminate the need for evidence selection and source authority.

## 5. Tool use and function calling reliability

LLMs can call tools, but tool use introduces new failure modes.

The model may choose the wrong tool, call the right tool with wrong arguments, ignore tool results, hallucinate tool outputs, or call tools in unsafe sequences.

The hard problem:

> How do we make probabilistic model decisions interact safely with deterministic tools?

Important directions:

- typed schemas
- argument validation
- tool-call planning
- tool-result verification
- retries and error handling
- read/write separation
- approval gates for side effects
- idempotency for writes

Interview phrase:

> Tool use is where LLM reliability becomes systems engineering.

## 6. Alignment and instruction hierarchy

Modern models receive many instruction sources:

- system instructions
- developer instructions
- user prompts
- retrieved documents
- tool outputs
- memory
- conversation history

The hard problem:

> How does the model follow the correct instruction hierarchy, especially when lower-trust content contains malicious or conflicting instructions?

Important cases:

- prompt injection from documents or webpages
- tool-output injection
- user attempts to override policy
- memory conflicts with current instructions
- enterprise policy conflicts

Good production principle:

> External content is data, not instructions.

## 7. Evaluation of frontier models

Evaluating LLMs is getting harder.

Benchmarks saturate. Benchmarks leak. Models can be trained on benchmark-like data. Some tasks are subjective. Some capabilities only appear in agentic settings. Some failures are rare but catastrophic.

The hard problem:

> How do we evaluate models in ways that predict real-world behavior?

Important directions:

- hidden evals
- adversarial evals
- real-world task suites
- agent trace evals
- long-horizon task evals
- domain-specific golden sets
- safety and misuse evals
- calibration and abstention metrics

Interview phrase:

> Final-answer accuracy is not enough; for agents we need to evaluate traces, tool calls, retrieval, uncertainty, and side effects.

## 8. Inference efficiency and serving cost

Frontier models are expensive to run.

The hard problem:

> How do we deliver high-quality answers at acceptable latency and cost?

Important directions:

- model routing
- smaller specialist models
- speculative decoding
- quantization
- distillation
- caching
- batching
- mixture-of-experts
- context compression
- adaptive thinking budgets

Production tradeoff:

> The best model is not always the biggest model. The best system routes the right task to the right capability at the right cost.

## 9. Data quality, synthetic data, and post-training

Pretraining data is finite, noisy, biased, duplicated, and increasingly AI-generated.

The hard problem:

> How do we keep improving models when high-quality human data is limited and synthetic data can amplify errors?

Important directions:

- curated high-quality datasets
- synthetic data generation
- rejection sampling
- human preference data
- reinforcement learning with verifiable rewards
- domain-specific post-training
- distillation from stronger models
- contamination detection

Risk:

Synthetic data can improve reasoning if generated and filtered well. It can also create model collapse, style homogenization, or hidden error amplification if used carelessly.

## 10. Interpretability and mechanistic understanding

LLMs work better than we understand.

We can observe behavior, but often cannot explain exactly why a model made a particular internal representation or decision.

The hard problem:

> How do we understand and control systems whose internal reasoning is distributed across billions or trillions of parameters?

Important directions:

- mechanistic interpretability
- feature attribution
- circuit analysis
- activation steering
- representation analysis
- model internals for safety monitoring

Production reality:

Interpretability is not yet strong enough to be the main safety layer. Most production safety still comes from external controls: evals, retrieval, tools, permissions, monitoring, and policy gates.

## 11. Multimodal grounding and world models

Models increasingly process text, images, audio, video, code, and structured data.

The hard problem:

> How do we make models reason reliably across modalities and connect language to the real world?

Failure modes:

- hallucinating image details
- weak spatial reasoning
- misreading charts or tables
- missing temporal sequence in video
- confusing visual similarity with semantic truth
- overconfident interpretation of ambiguous signals

Important directions:

- better multimodal encoders
- grounded tool use
- visual verification
- structured extraction from documents
- multimodal evals

## 12. Security and misuse resistance

LLMs can assist with cyber, persuasion, fraud, social engineering, bio research, and automated abuse.

The hard problem:

> How do we preserve beneficial capability while preventing dangerous misuse?

Important directions:

- capability thresholds
- abuse monitoring
- refusal training
- tool restrictions
- user verification for high-risk tools
- secure deployment
- red teaming
- incident response

This becomes much harder when LLMs are embedded in agents that can act through tools.

## Interview-ready summary

A strong answer:

> The hard problems in LLMs are not just scaling. They include reasoning reliability, difficulty-aware routing, hallucination and calibration, long-context reliability, safe tool use, instruction hierarchy, evaluation, inference efficiency, data quality, interpretability, multimodal grounding, and misuse resistance. In production, the model is only one part of the system. The strongest designs combine model capability with routing, retrieval, tools, verifiers, permissions, evals, monitoring, and deterministic guardrails.
