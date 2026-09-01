# Component Versioning

Read this reference when product modules must be developed, released, combined, or rolled back independently.

## Release Unit

Use an independently valuable and independently testable product capability as the component boundary. Examples include a route selector, WBS view, execution network, task-detail surface, or workflow adapter. A visual primitive is too small; an entire business direction is usually too large.

Each component declares:

- `component_id` and owning product direction;
- `version` and immutable source or artifact reference;
- `contract_version` for its public inputs, outputs, events, and persisted data;
- compatible dependency ranges;
- component-level tests and acceptance evidence;
- a known-good rollback target and any data migration constraint.

## Development and Integration

- Give each component change an isolated branch or worktree, allowed file scope, deliverable, and test set.
- Keep shared contracts outside component internals. Consumers depend on the published contract, not private implementation details.
- Pin the assembled product in a composition manifest. The manifest is the release truth for which component versions run together.
- Run component tests first, contract tests second, and product-level integration tests last.
- A breaking contract change requires a new contract version and coordinated consumer releases. It cannot be hidden inside a nominal component-only rollback.

## Rollback Rule

Rollback changes the target component's pinned version in the composition manifest and re-runs compatibility and smoke tests. Preserve every unrelated component version. Escalate to a coordinated rollback only when persisted data, a shared contract, or another component was changed incompatibly.

## Minimum Manifest

```yaml
product_release: example-product@1.4.0
components:
  route-workspace:
    version: 1.0.0
    source_ref: <immutable commit or artifact>
    contract_version: route-workspace/v1
    depends_on:
      task-projection: ">=1.2 <2"
    rollback_to: 0.9.3
compatibility_status: VERIFIED
```

Use `UNKNOWN` instead of inventing an unavailable version, compatibility result, source reference, or rollback target.

