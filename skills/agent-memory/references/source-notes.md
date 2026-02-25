# Source Notes: What Memory Is For

This file anchors memory policy in frontier labs' public guidance and research.

## Frontier Labs / Agency Blogs

1. OpenAI - *Inside our in-house data agent*  
   Link: https://openai.com/index/inside-our-in-house-data-agent/  
   Relevance: Describes a layered architecture where memory stores corrections and filters across interactions, i.e., behavior-shaping context that persists.

2. OpenAI - *A practical guide to building agents*  
   Link: https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/  
   Relevance: Emphasizes maintaining and transferring state (including latest conversation context) across handoffs.

3. OpenAI Agents SDK docs/cookbook (context personalization)  
   Link: https://developers.openai.com/cookbook/examples/agents_sdk/context_personalization  
   Relevance: Shows explicit memory lifecycle (capture, consolidate, inject) for consistent future behavior.

4. Anthropic - *Context management*  
   Link: https://www.anthropic.com/news/context-management  
   Relevance: Presents memory as persisted context/state beyond transient context windows.

5. Anthropic Engineering - *How we built our multi-agent research system*  
   Link: https://www.anthropic.com/engineering/multi-agent-research-system  
   Relevance: Discusses task-state persistence and memory/scratchpad strategies for long-horizon agent work.

## Research Papers

6. Reflexion (Shinn et al., 2023)  
   Link: https://arxiv.org/abs/2303.11366  
   Relevance: Uses episodic memory of reflections to improve subsequent attempts.

7. Voyager (Wang et al., 2023)  
   Link: https://arxiv.org/abs/2305.16291  
   Relevance: Skill library acts as reusable long-term memory for new tasks.

8. Generative Agents (Park et al., 2023)  
   Link: https://arxiv.org/abs/2304.03442  
   Relevance: Memory stream + reflection + retrieval underpins coherent long-term behavior.

9. MemGPT (Packer et al., 2023)  
   Link: https://arxiv.org/abs/2310.08560  
   Relevance: Treats memory hierarchically to overcome finite context limits.

10. ReadAgent (Google DeepMind, 2025)  
    Link: https://deepmind.google/research/publications/74917/  
    Relevance: Uses extracted "gist" memories for scalable long-context reasoning.

## Policy Implication

Across these sources, memory is consistently used as:
- persistent state for future execution quality
- retrieval substrate for non-obvious constraints
- behavior-shaping continuity across sessions/tasks

Not as:
- a substitute for version control
- a changelog or audit history of edits

