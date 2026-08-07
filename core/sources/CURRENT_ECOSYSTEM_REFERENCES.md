# Current Ecosystem References

**Reference snapshot date:** 2026-08-07

These sources informed the Swarm OS design. They are references, not dependencies, and should be refreshed during future commissioning because agent platforms evolve quickly.

## OpenAI

- OpenAI Agents SDK — Agent orchestration: https://openai.github.io/openai-agents-python/multi_agent/
  - Useful pattern: manager/orchestrator agent retaining control versus specialist handoffs.
- OpenAI Agents SDK — Handoffs: https://openai.github.io/openai-agents-python/handoffs/
  - Useful pattern: explicit handoff metadata and controlled context transfer.
- OpenAI Agents SDK repository examples: https://github.com/openai/openai-agents-python
  - Useful pattern: routing, agents-as-tools, and specialist decomposition.

## Anthropic / Claude Code

- Claude Code — custom subagents: https://code.claude.com/docs/en/sub-agents
  - Useful pattern: isolated specialized contexts, scoped tools, project-level agent definitions, foreground/background execution.
- Claude Code — memory / CLAUDE.md: https://code.claude.com/docs/en/memory
  - Useful pattern: persistent project instructions separate from conversation memory; concise durable memory.
- Claude Code — hooks: https://code.claude.com/docs/en/hooks-guide
  - Useful pattern: move deterministic enforcement out of prompts when a machine-enforceable hook is available.
- Anthropic Claude Code repository: https://github.com/anthropics/claude-code

## GitHub

- GitHub Copilot repository custom instructions: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
  - Useful pattern: `AGENTS.md` and repository-scoped instructions.
- GitHub custom agents overview: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents
  - Useful pattern: specialized agent profiles with scoped tools and prompts.
- GitHub Awesome Copilot agents: https://github.com/github/awesome-copilot
  - Useful pattern: public library of orchestrator, researcher, implementer, reviewer, documentation, security, and domain agent profiles.
- Agent creation guidance in Awesome Copilot: https://github.com/github/awesome-copilot/blob/main/instructions/agents.instructions.md
  - Useful pattern: explicit role purpose, minimal tool sets, QA, and selective handoffs.

## How to use these references

Prefer adapting architectural patterns over copying prompt prose. Recheck license and current platform behavior before importing any third-party agent file.
