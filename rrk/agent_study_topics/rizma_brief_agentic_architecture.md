# Rizma Brief: Agentic Architecture for an HSP-Centric Conversational News Service

## Executive Summary

Rizma Brief is evolving from a “news app with chat” into a **conversational emotional-safety layer over current events**. The user does not simply ask for headlines. The user asks for orientation, explanation, reassurance, context, follow-up, and sometimes news coverage. The system should therefore be architected less like a feed and more like a bounded conversational agent with optional news retrieval.

The core architecture should resemble the best lesson from Claude Code: one main agentic loop inside a strong harness. The main agent owns the user conversation, interprets intent, assembles context, chooses whether live news is needed, streams a response, and maintains the desired emotional tone. Optional subagents or specialized services can support it: news retrieval, source verification, tone/sensitivity review, factuality checks, and content-safety filtering.

The goal is not to build a swarm of agents for its own sake. The goal is to create a reliable, calm, factually grounded, emotionally adjustable assistant for highly sensitive people.

The shortest product architecture statement is:

> **Rizma Brief should be a calm conversational agent first, with news retrieval and sensitivity-aware grounding as optional capabilities.**

---

## 1. Product Reframing

The original product idea was an HSP-friendly news service: users could stay informed without emotional overload. That is still the core emotional promise. But the product is becoming more conversational. The user may not always want “news.” Sometimes the user wants an explanation, a gentle summary, a grounded answer, a low-intensity briefing, a follow-up question, or help understanding whether something matters.

This means the system should not always start with news retrieval. It should first understand the user’s intent.

A user might ask:

> “What happened with Iran today?”

That probably requires current news retrieval.

But a user might also ask:

> “Why do ceasefire talks always collapse?”

That may require historical explanation, maybe with some current context, but not necessarily a full news search.

Or:

> “I saw a scary headline. Can you explain it calmly?”

That requires tone control and emotional safety before it requires exhaustive coverage.

So the architecture should treat news as a tool, not as the whole product.

---

## 2. Core Design Principle

The main principle should be:

> **One main conversational agent owns the user experience. Specialized agents or services support it only when they add clear value.**

This avoids unnecessary complexity. It also protects the emotional continuity of the product. HSP users may be sensitive not just to content, but also to tone shifts, contradictions, abruptness, or overproduction of alarming details. If too many agents directly speak to the user, the experience may feel fragmented.

The main agent should be responsible for:

- understanding the user’s request
- deciding whether current news retrieval is required
- selecting calm, balanced, or brave intensity
- assembling conversational context
- invoking tools or subagents
- streaming the final answer
- maintaining emotional continuity
- explaining uncertainty
- citing sources when news is used

Specialized agents should mostly produce internal artifacts, not user-facing prose. The final answer should be composed by the main agent.

---

## 3. Main Agent Responsibilities

The main Rizma Brief agent is the user-facing conversational agent. It should behave like a calm, grounded, emotionally aware explainer.

It should first classify the user’s intent. The user may be asking for breaking news, background explanation, emotional reassurance, comparison, a timeline, source evaluation, or a follow-up to a previous topic. The agent should not automatically retrieve current news for every query. Retrieval should be triggered when freshness matters or when the user explicitly asks for updates.

The main agent should also own tone. Rizma Brief’s modes — Calm, Balanced, and Brave — should not just be decorative labels. They should affect the response style.

Calm mode should minimize alarming framing, reduce graphic detail, explain uncertainty, and focus on practical meaning.

Balanced mode should provide a more standard factual answer with moderate emotional cushioning.

Brave mode can include more direct language, deeper geopolitical context, and more detail, while still avoiding sensationalism.

The main agent should also know when to abstain or soften. For example, if sources are uncertain, it should say so. If a topic is speculative, it should separate confirmed facts from claims. If the content is potentially distressing, it should preview the topic before going deeper.

---

## 4. Suggested High-Level Architecture

A useful architecture is:

```text
User message
  → conversation/session context
  → main Rizma agent
  → intent and intensity decision
  → optional retrieval or specialist checks
  → grounded response assembly
  → tone/safety pass
  → streaming answer with citations when relevant
```

The system can be implemented as one main orchestration service with several tools and optional specialist workers. It does not need to be a fully autonomous multi-agent swarm.

The key architectural pattern is similar to Claude Code:

> **The main agent reasons. The harness controls context, tools, retrieval, safety, source authority, and logging.**

For Rizma Brief, the harness should own:

- source selection
- news API calls
- retrieval freshness
- citation formatting
- source reliability metadata
- tone mode constraints
- distressing-content policy
- caching and rate limits
- user preference memory
- observability and evaluation

The LLM should not be the source of truth for current facts. If the answer depends on current news, the system should retrieve current sources.

---

## 5. Tool and Subagent Breakdown

The first design decision is whether these should be tools, services, or subagents.

A simple deterministic call should be a tool. For example, `search_news(query, date_range, sources)` is a tool. `fetch_article(url)` is a tool. `get_user_tone_preference(user_id)` is a tool. `save_feedback(rating, reason)` is a tool.

A specialized reasoning task may justify a subagent or internal LLM worker. For example, a News Retrieval Agent could transform a vague user query into search queries, retrieve coverage, cluster articles, and return a compact evidence brief. A Tone/Sensitivity Reviewer could inspect a draft and flag phrases that are too abrasive for Calm mode. A Factuality Checker could compare claims in the draft against retrieved evidence and flag unsupported assertions.

The main rule is:

> **Use subagents for bounded reasoning artifacts. Use tools for deterministic operations.**

The user should not experience a committee of agents. The user should experience one calm assistant.

---

## 6. Proposed Components

### Main Conversational Agent

The main agent owns the user interaction. It decides whether the user is asking for current news, background context, emotional grounding, explanation, or follow-up. It streams the response and controls the final tone.

It should output a response that is conversational, not a newspaper article. When news is relevant, it should integrate coverage naturally:

> “The latest reports suggest X. The important context is Y. In calm terms, this means Z. There is still uncertainty around A and B.”

### News Retrieval Worker

The news worker should be invoked only when current coverage is needed. It should search across configured news APIs or sources, deduplicate stories, cluster related coverage, rank by freshness and reliability, and return an evidence packet.

The evidence packet should include:

- topic summary
- source list
- publication time
- key claims
- where sources agree
- where sources differ
- uncertainty level
- suggested citations

This worker should not write the final user-facing answer. It should return structured evidence to the main agent.

### Source and Factuality Checker

This component checks whether the draft answer is supported by retrieved evidence. It should identify unsupported claims, overconfident wording, stale information, missing citations, and claims that need hedging.

For example, if the draft says “the ceasefire has collapsed,” but sources only say “talks are strained,” the checker should flag the claim and suggest softer wording.

This is especially important because the product promise is not only emotional safety but also factual integrity.

### Tone and Sensitivity Reviewer

This component checks whether the draft matches the selected intensity mode.

In Calm mode, it should flag sensational language, graphic detail, doom framing, excessive speculation, and emotionally loaded verbs. It should not remove important facts, but it should suggest gentler wording.

In Balanced mode, it should allow more directness while avoiding unnecessary emotional amplification.

In Brave mode, it can permit more detail and sharper analysis, but still avoid manipulative or sensational framing.

### User Preference and Memory Service

This should store stable, useful preferences, not sensitive or speculative facts. It might remember that a user prefers Calm mode by default, likes short summaries first, wants citations, or prefers “what this means” sections.

It should not store medicalized labels or inferred psychological traits unless the user explicitly asks. The product is HSP-centric, but memory should remain respectful and minimal.

A good memory policy is:

> **Remember preferences, not vulnerabilities.**

### Safety and Escalation Layer

The system should handle distressing topics carefully. It should avoid graphic detail unless necessary and requested. It should provide content warnings for severe violence, suicide, sexual violence, or child harm. It should not manipulate the user into consuming more news.

The product should also know when not to answer as news. If a user expresses acute distress, the system should shift from news explanation to supportive grounding and, when appropriate, crisis resources.

---

## 7. Example Flow: Current News Query

User:

> “What happened with the Iran negotiations today? Explain calmly.”

The main agent identifies that freshness matters. It invokes the news retrieval worker. The retrieval worker searches current sources and returns an evidence packet: latest developments, key actors, what is confirmed, what is uncertain, and citations.

The main agent drafts a Calm-mode answer. It avoids dramatic phrasing like “spiraling toward war” unless directly supported and necessary. It might say:

> “The talks appear strained, but not necessarily over. The main disagreement seems to be X. The practical meaning is that both sides are still signaling pressure while leaving some room for negotiation.”

The factuality checker verifies that the claims are supported. The tone reviewer checks that the answer is calm and not alarmist. The final response is streamed to the user with citations.

---

## 8. Example Flow: Background Explanation

User:

> “Why are ceasefire negotiations so hard?”

The main agent may decide that current retrieval is optional. This is mostly an explanatory question. It can answer from general knowledge, or retrieve if the user’s session context suggests a current conflict.

The answer should be conversational:

> “Ceasefire talks are hard because each side wants safety guarantees, but those guarantees often look threatening to the other side. There is also a trust problem: even if leaders agree, local actors may not comply.”

If current examples are relevant, the agent can add:

> “If you want, I can also connect this to the latest coverage.”

The architecture should avoid unnecessary news retrieval when the user is really asking for conceptual grounding.

---

## 9. Example Flow: Emotional Safety Query

User:

> “I saw a scary headline and now I feel overwhelmed. Can you explain whether I need to worry?”

The main agent should treat this primarily as an emotional-safety and explanation task. It may ask for the headline or summarize based on what the user provides. If it needs current facts, it can retrieve them, but the first obligation is to avoid escalating the user’s distress.

A good response pattern is:

> “Let’s slow it down. A headline is often written to sound urgent. I’ll separate what is confirmed, what is uncertain, and what it means for you practically.”

This is where Rizma Brief is distinct from a normal news chatbot. It is not just summarizing content. It is shaping the information experience.

---

## 10. Source Authority and Retrieval Policy

Rizma Brief should have an explicit source policy. The system should know which sources are preferred for breaking news, which are useful for analysis, which are lower-confidence, and when to avoid over-relying on a single source.

A strong evidence packet should distinguish:

- confirmed facts
- official statements
- claims from one side
- expert analysis
- speculation
- old background context
- live updates

The main agent should never present a single unverified claim as settled fact. It should say things like:

> “According to early reports...”

or:

> “Several outlets report X, but Y remains unclear.”

This is especially important for emotionally sensitive users because false certainty can increase distress.

---

## 11. Guardrails

Rizma Brief needs guardrails in several dimensions.

Factual guardrails should prevent unsupported claims, stale information, fake citations, and overconfident statements.

Emotional guardrails should prevent sensationalism, doom framing, graphic detail, and unnecessarily alarming language.

Product guardrails should prevent addictive news consumption patterns. The assistant should not push the user to keep reading distressing content.

Privacy guardrails should limit what is remembered about the user. The system can remember preferences, but should avoid inferring or storing sensitive psychological profiles.

Action guardrails are simpler than in Claude Code because Rizma Brief does not normally modify external systems. But if future versions send emails, schedule reminders, or post summaries, those actions should require explicit confirmation and deterministic payload validation.

---

## 12. Evaluation Strategy

Rizma Brief should be evaluated on more than answer quality.

It needs factuality evaluations:

- Are claims supported by sources?
- Are citations accurate?
- Does the answer distinguish fact from uncertainty?
- Does it retrieve fresh news when freshness matters?
- Does it avoid retrieval when not needed?

It also needs emotional-safety evaluations:

- Is Calm mode actually calm?
- Does the response avoid sensational language?
- Does it preserve important facts while reducing emotional overload?
- Does it avoid graphic detail unless necessary?
- Does it help the user understand practical meaning?

And it needs product evaluations:

- Does the user feel informed but not overwhelmed?
- Do users trust the citations?
- Do users continue using it for follow-up questions?
- Are there fewer cases of panic, confusion, or doom-scrolling?

A key metric could be:

> **Informed calm:** the user understands the issue better without feeling emotionally flooded.

---

## 13. Suggested Implementation on GCP

A practical GCP architecture could use:

- Cloud Run for the FastAPI backend
- Vercel or Cloud Storage + Cloud CDN for the frontend
- Cloud SQL or Firestore for users, sessions, preferences, and feedback
- Cloud Storage for article snapshots, transcripts, and audio files
- Secret Manager for news API keys and model provider keys
- Cloud Tasks or Pub/Sub for async retrieval, summarization, and evaluation jobs
- Vertex AI or external LLM APIs for generation and evaluation
- BigQuery for analytics and eval traces
- Cloud Logging and Monitoring for observability

The backend should expose a streaming chat endpoint. The main agent can start streaming once it has enough context, but for current news queries it may first need retrieval. For latency, the system can stream an initial acknowledgement:

> “I’ll check the latest coverage and keep this calm.”

Then retrieve, assemble, verify, and continue streaming the answer.

---

## 14. Recommended Agent Pattern

The recommended pattern is not a large multi-agent swarm. It is:

> **Main conversational agent + bounded specialist workers + deterministic tools.**

The main agent owns the user experience. Specialist workers produce structured artifacts. Deterministic tools retrieve data, fetch articles, store preferences, and log events. The harness enforces safety, source policy, tone policy, and observability.

A useful architecture is:

```text
Main Rizma Agent
  ├── News Retrieval Worker
  ├── Factuality / Citation Checker
  ├── Tone and Sensitivity Reviewer
  ├── User Preference Memory Service
  └── Deterministic Tools
        ├── search_news
        ├── fetch_article
        ├── retrieve_session_context
        ├── save_feedback
        └── log_eval_trace
```

Subagents should not all speak to the user. They should return internal artifacts to the main agent.

---

## 15. FDE / RRK Relevance

Rizma Brief is a good FDE-style example because it demonstrates applied GenAI architecture beyond a toy chatbot.

It includes:

- intent classification
- retrieval decisioning
- RAG over current news
- source authority and citation handling
- tone control
- safety guardrails
- user preference memory
- streaming UX
- evals for factuality and emotional safety
- bounded agent orchestration
- cloud deployment concerns

The key FDE framing is:

> “I would not build Rizma Brief as a generic chatbot. I would build it as a controlled conversational agent with retrieval, source authority, tone governance, and optional specialist workers. The main agent owns the user experience, while the harness controls what information is retrieved, how claims are grounded, how distressing content is softened, and how the system is evaluated.”

---

## 16. Interview-Ready Summary

Rizma Brief should be designed as an HSP-centric conversational agent, not merely a news summarizer. The main agent owns the conversation and streams a calm, grounded answer. It decides whether the user needs current news retrieval, background explanation, emotional grounding, or follow-up. When current facts matter, it invokes a news retrieval worker that returns structured evidence. A factuality checker verifies claims against sources, and a tone/sensitivity reviewer ensures the answer matches Calm, Balanced, or Brave mode.

The architecture should borrow the best lesson from Claude Code: a simple main agent loop inside a strong harness. The LLM can reason and compose, but the harness owns retrieval, source authority, tone rules, safety policies, memory boundaries, logging, and evaluation. Subagents are useful only when they produce bounded internal artifacts, such as evidence packets or tone-review feedback. The user should experience one coherent assistant, not a committee of agents.

The shortest version:

> **Rizma Brief is a calm conversational agent with optional news grounding, not a raw news feed and not an uncontrolled multi-agent swarm.**

---

## Sources and Notes

This architecture note is based on the product direction discussed for Rizma Brief: an HSP-centric, conversational news and explanation service with Calm / Balanced / Brave modes, cited sources, follow-up chat, and emotional-overload reduction.

Generated with assistance from ChatGPT 5.5. Edited for FDE/RRK interview preparation.
