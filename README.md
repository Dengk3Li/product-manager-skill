# Product Manager Skill Suite

English | [简体中文](README.zh-CN.md)

[![CI](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Dengk3Li/product-manager-skill/actions/workflows/ci.yml)

An Agent Skill suite that connects customer evidence and business goals to product decisions, hierarchical requirements, roadmaps, delivery coverage, and outcome feedback without taking over technical architecture.

## Quick start

Install with the open skills CLI:

```bash
npx skills add Dengk3Li/product-manager-skill --skill product-manager
npx skills add Dengk3Li/product-manager-skill --skill product-roadmap
npx skills add Dengk3Li/product-manager-skill --skill product-requirements
```

Then ask your agent:

```text
Use $product-manager to decide whether this request needs a PRD.
Use $product-manager to define the scope and acceptance for this release.
Use $product-manager to split this roadmap only where outputs are independently valuable.
Use $product-roadmap to create an evidence-based Now/Next/Later roadmap.
Use $product-requirements to approve one requirement baseline, trace delivery automatically, and ask me only for material decisions.
```

The core skill owns product logic and routes detailed roadmap or requirement-traceability work to the matching companion skill.

Audit a requirement model without stopping delivery on warnings:

```bash
python3 skills/product-requirements/scripts/check_requirements_traceability.py \
  requirements-traceability.json --phase delivery
```

## What it does

Product Manager helps an agent:

- connect customer evidence, commercial context, strategy, and product outcomes;
- identify the user or business outcome behind a request;
- compare opportunities and alternatives before committing to a solution;
- separate required scope, optional scope, and explicit non-goals;
- prioritize with explicit evidence, confidence, risk, and opportunity cost;
- build stakeholder-readable roadmaps without inventing dates;
- give requirements durable IDs, hierarchy, supporting relationships, and observable acceptance;
- audit implementation coverage, blockers, verification, and human acceptance against approved requirements;
- compare observed results with the hypothesis after release;
- preserve `UNKNOWN` when authority, ownership, provenance, or release state is not verified;
- hand architecture, implementation, and task administration to their owning roles.

It is decision support, not a general-purpose project-management framework.

## The problem this suite solves

Coding agents often start from a sentence that mixes a business goal, a proposed feature, and an implementation guess. The resulting code can be technically complete while solving the wrong problem. Later, nobody can reliably answer which original requirement a module satisfies or why a supporting requirement exists.

The usual correction creates a second problem: every item receives a status, gate, approval, and manual acceptance step. Humans spend time reviewing generated process records instead of making product decisions.

This suite keeps a durable chain from business outcome to requirement to implementation evidence. The human approves the product baseline once. Agents maintain hierarchy, mappings, delivery state, evidence, and blocker summaries. The workflow returns to a human only when scope, priority, risk, cost, user-visible behavior, or release acceptance needs judgment.

Small settled work stays small. Multi-part work gains enough structure to remain traceable without becoming a parallel project-management system.

## Human review budget

| Moment | Human responsibility | Agent responsibility |
|---|---|---|
| Before consequential work | Approve one baseline and settle material open choices | Research facts, draft the hierarchy, connect supporting requirements, and surface only material decisions |
| During delivery | Decide only on scope or product changes | Maintain module mappings, evidence, coverage, and blocker summaries |
| At module or release acceptance | Judge the delivered outcome once | Verify required criteria from tests, runtime observations, and contracts |

Enablers inherit the baseline and release decision unless they introduce a separate product consequence.

## Planning modes

| Mode | Use it when | Typical output |
|---|---|---|
| **Direct** | One clear result, one write set, no material product decision left open | Outcome, scope, acceptance, next action |
| **Coordinated** | Two or more independently valuable outputs, multiple owners, or a real dependency | Compact brief, L1/L2 split, actual dependencies |
| **Controlled** | Privacy, compliance, public-release, irreversible-cost, or user-trust consequences | Product authority, risk, release boundary, and acceptance evidence |

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

The skill selects **Controlled** because public release and persistent-data migration change the product commitment. It states the decision authority, user and business risk, release boundary, and evidence required before release, then routes technical controls to their owning workflows.

## How it works

1. Read customer, product, business, roadmap, delivery, and decision evidence.
2. Frame the target customer, problem, outcome, business value, constraints, and one reviewable baseline.
3. Compare opportunities and alternatives, then identify the riskiest assumption.
4. Recommend and shape the smallest useful release.
5. Approve the baseline once and route architecture placement to the system architect.
6. Let agents maintain requirement coverage, evidence, and blocker summaries during delivery.
7. Verify required outcomes, request one module or release decision, and revisit the product hypothesis after release.

The requirements checker supports `report`, `align`, `delivery`, and `acceptance` phases. Structural contradictions always block. Delivery evidence gaps normally warn. Acceptance blocks only required outcomes that remain unverified or lack the release-level human decision.

## Role boundary

| Role | Owns |
|---|---|
| Product manager | Problem, priority, scope, non-goals, release boundary, acceptance |
| Product roadmap | Strategy-to-outcome sequencing, horizons, confidence, and roadmap feedback |
| Product requirements | One approved baseline, requirement hierarchy, automatic delivery traceability, exception reporting, and release-level acceptance |
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
- pre-implementation requirement alignment and post-build coverage or blocker reviews;
- plans that have accumulated tasks but still lack a clear decision.

Do not invoke it again for:

- already-scoped implementation;
- routine bug fixes;
- document cleanup;
- isolated acceptance checks that do not need the requirement baseline;
- task-card maintenance;
- branch or worktree lifecycle operations.

## Package contents

```text
.codex-plugin/plugin.json
skills/product-manager/
  SKILL.md
  agents/openai.yaml
  references/product-sources.md
skills/product-roadmap/
  SKILL.md
  agents/openai.yaml
  references/roadmap-method.md
skills/product-requirements/
  SKILL.md
  agents/openai.yaml
  assets/requirements-traceability.template.json
  references/requirements-model.md
  scripts/check_requirements_traceability.py
tests/test_package.py
tests/test_requirements_traceability.py
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
- [Atlassian: Agile roadmaps](https://www.atlassian.com/agile/product-management/roadmaps)
- [Atlassian: Product discovery](https://www.atlassian.com/agile/product-management/discovery)
- [Product Talk: Discovering solutions](https://www.producttalk.org/discovering-solutions/)

See [product-sources.md](skills/product-manager/references/product-sources.md) for the rule-by-rule adaptation notes.

## Development

Run the package tests:

```bash
python3 -m unittest discover -s tests -v
```

Validate the skill and plugin manifests with the corresponding creator tools:

```bash
python3 <skill-creator>/scripts/quick_validate.py skills/product-manager
python3 <skill-creator>/scripts/quick_validate.py skills/product-requirements
python3 <plugin-creator>/scripts/validate_plugin.py .
```

The package has no runtime dependency beyond a compatible Agent Skills host.

## License

This repository is publicly visible but does not currently grant an open-source license.
