<planning_context>
**Phase:** 3
**Mode:** standard

<files_to_read>
- .planning/STATE.md (Project State)
- .planning/ROADMAP.md (Roadmap)
- .planning/REQUIREMENTS.md (Requirements)
- .planning/phases/03-probabilistic-api-visualization/03-CONTEXT.md (USER DECISIONS from /gsd-discuss-phase)
- .planning/phases/03-probabilistic-api-visualization/03-RESEARCH.md (Technical Research)
- .planning/phases/03-probabilistic-api-visualization/03-VALIDATION.md (Validation Strategy)
</files_to_read>



**Phase requirement IDs (every ID MUST appear in a plan's `requirements` field):** REL-03, REL-04

**Project instructions:** Read ./AGENTS.md if exists — follow project-specific guidelines
**Project skills:** Check .claude/skills/ or .agents/skills/ directory (if either exists) — read SKILL.md files, plans should account for project skill rules

</planning_context>

<downstream_consumer>
Output consumed by /gsd-execute-phase. Plans need:
- Frontmatter (wave, depends_on, files_modified, autonomous)
- Tasks in XML format with read_first and acceptance_criteria fields (MANDATORY on every task)
- Verification criteria
- must_haves for goal-backward verification
</downstream_consumer>

<deep_work_rules>
## Anti-Shallow Execution Rules (MANDATORY)

Every task MUST include these fields — they are NOT optional:

1. **`<read_first>`** — Files the executor MUST read before touching anything.
2. **`<acceptance_criteria>`** — Verifiable conditions that prove the task was done correctly.
3. **`<action>`** — Must include CONCRETE values, not references.
</deep_work_rules>
