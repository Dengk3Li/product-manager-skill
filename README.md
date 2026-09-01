# Product Manager Skill

English | [简体中文](README.zh-CN.md)

[![CI](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml)

An Agent Skill that turns ambiguous product requests into clear scope and acceptance without producing a PRD for every change.

## Quick start

Install with the open skills CLI:

```bash
npx skills add Dengk3Li/product-manager-skill --skill product-manager
```

Then ask your agent:

```text
Use $product-manager to decide whether this request needs a PRD.
Use $product-manager to define the scope and acceptance for this release.
Use $product-manager to split this roadmap only where outputs are independently valuable.
```

The skill chooses one of three planning modes, writes the smallest artifact that resolves the decision, and stops once implementation can proceed.

## What it does

Product Manager helps an agent:

- identify the user or business outcome behind a request;
- separate required scope, optional scope, and explicit non-goals;
- choose a planning depth that matches the actual coordination need;
- define acceptance as observable results;
- preserve `UNKNOWN` when authority, ownership, provenance, or release state is not verified;
- hand architecture, implementation, and task administration to their owning roles.

It is decision support, not a general-purpose project-management framework.

## Why it exists

Product work with coding agents tends to fail in two opposite ways.

A small, settled change can trigger a full PRD, a multi-level WBS, risk gates, task cards, and several review documents. The planning overhead becomes larger than the work.

A broad request can fail differently: the agent starts implementing before the outcome, release boundary, and non-goals are clear. Scope expands while product, architecture, and delivery decisions get mixed together.

This skill uses proportional planning. Structure is added only when it resolves a real product decision, coordinates independently valuable outputs, or controls a confirmed risk.

## Planning modes

| Mode | Use it when | Typical output |
|---|---|---|
| **Direct** | One clear result, one write set, no material product decision left open | Outcome, scope, acceptance, next action |
| **Coordinated** | Two or more independently valuable outputs, multiple owners, or a real dependency | Compact brief, L1/L2 split, actual dependencies |
| **Controlled** | Public release, data migration, security, privacy, authority changes, destructive action, or conflicting writers | Product decision plus the required controls, review, and rollback |

Controlled work does not automatically need deeper decomposition. A single high-risk deliverable can remain one task.

## Examples

### Keep a small change small

```text
Change the settings-page button from “Save” to “Submit”. Also write a full PRD,
a three-level WBS, a risk gate, and task cards.
```

The skill selects **Direct**. It limits the scope to the label, preserves the existing save behavior, and defines a small acceptance check. It does not create the extra planning artifacts because they do not resolve a product decision.

### Coordinate independent outcomes

```text
Add a research board and import the history from the old project.
```

The board and the import can be built and accepted separately. The skill selects **Coordinated**, writes one short brief, and records the real ordering or data dependency between them.

### Add controls without inventing a large WBS

```text
Publish the dataset and migrate existing user records to the new schema.
```

The skill selects **Controlled** because public release and persistent-data migration change the release boundary. It adds ownership, rollback, and review requirements while keeping the task split tied to actual deliverables.

## How it works

1. Read the existing product, code, task, and decision context.
2. Find the unresolved question that can change the outcome, scope, acceptance, or release boundary.
3. Ask only for information that changes that decision.
4. Select Direct, Coordinated, or Controlled.
5. Deliver the decision and exit product shaping.

The skill re-enters product work only when product intent or the release boundary changes materially.

## Role boundary

| Role | Owns |
|---|---|
| Product manager | Problem, priority, scope, non-goals, release boundary, acceptance |
| System architect | Module placement, presentation budget, file ownership, shared surfaces, interfaces |
| Implementer | Code and tests inside the agreed boundary |
| Task system | Authorized tracking, assignment, and cross-session handoff |

Product clarification does not authorize task creation or code changes.

For module ownership and integration contracts, use the companion [System Architect Skill](https://github.com/Dengk3Li/system-architect-skill).

## When to use it

Use this skill for:

- ambiguous feature requests;
- PRDs, roadmaps, prioritization, and release scope;
- feature decomposition with independently valuable outcomes;
- product decisions that affect risk or release controls;
- plans that have accumulated tasks but still lack a clear decision.

Do not invoke it again for:

- already-scoped implementation;
- routine bug fixes;
- document cleanup;
- acceptance checks;
- task-card maintenance;
- branch or worktree lifecycle operations.

## Package contents

```text
.codex-plugin/plugin.json
skills/product-manager/
  SKILL.md
  agents/openai.yaml
  references/component-versioning.md
  references/product-sources.md
tests/test_package.py
```

`SKILL.md` is the runtime instruction set. The repository README is written for people evaluating or installing the skill.

## Design references

The skill adapts ideas from:

- [GOV.UK: Start by learning user needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)
- [Intercom: Start with the problem](https://www.intercom.com/blog/intercom-product-principles-start-with-the-problem/)
- [Intercom: Deliver outcomes](https://www.intercom.com/blog/product-principles-deliver-outcomes/)
- [SVPG: Four Big Risks](https://www.svpg.com/four-big-risks/)
- [Basecamp Shape Up: Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03)
- [Intercom: Keep it simple](https://www.intercom.com/blog/intercom-product-principles-keep-it-simple/)
- [GOV.UK: Product manager](https://www.gov.uk/service-manual/the-team/product-manager)
- [Atlassian: Product requirements template](https://www.atlassian.com/software/confluence/templates/product-requirements)

See [product-sources.md](skills/product-manager/references/product-sources.md) for the rule-by-rule adaptation notes.

## Development

Run the package tests:

```bash
python3 -m unittest discover -s tests -v
```

Validate the skill and plugin manifests with the corresponding creator tools:

```bash
python3 <skill-creator>/scripts/quick_validate.py skills/product-manager
python3 <plugin-creator>/scripts/validate_plugin.py .
```

The package has no runtime dependency beyond a compatible Agent Skills host.

## License

This repository is publicly visible but does not currently grant an open-source license.
