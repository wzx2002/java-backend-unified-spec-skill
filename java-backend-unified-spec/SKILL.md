---
name: java-backend-unified-spec
description: Unified standard for Java backend project design, implementation, refactoring, and code review. Use when Codex needs to build or modify a Java backend that should follow module-first organization, preferred top-level module naming `infrastructure / persistence / business / web`, `interfaces` for multi-entry projects, optional `integration` for heavy third-party integrations, detailed naming and commenting rules, explicit security baselines, maintainability governance, and full module API regression after each module is completed.
---

# Java Backend Unified Spec

## Rule Levels

Use the following rule levels across reference files:

- `MUST`: default mandatory baseline for new projects and for modified areas in existing projects
- `RECOMMENDED`: preferred default; legacy projects may adopt incrementally based on cost and risk
- `OPTIONAL`: choose according to business type, traffic model, team size, and compliance needs

## Workflow

1. Split the work by project goal or business requirement into modules first. Do not flatten the project into one global `controller / service / repo` structure.
2. Read only the relevant reference file before designing or editing code:
   - architecture and module boundaries: [references/architecture-and-boundaries.md](references/architecture-and-boundaries.md)
   - naming, comments, validation, and code quality: [references/coding-standards.md](references/coding-standards.md)
   - security, third-party integration, concurrency, testing, and delivery: [references/security-integration-and-delivery.md](references/security-integration-and-delivery.md)
   - secure baseline for secrets, sensitive data, upload/download, callback protection, and release checks: [references/secure-baseline.md](references/secure-baseline.md)
   - maintainability governance for compatibility, ADR, module README, and quality gates: [references/evolution-and-governance.md](references/evolution-and-governance.md)
   - reusable templates and the single source of truth for PR, review, delivery, and release checklists: [references/templates-and-checklists.md](references/templates-and-checklists.md)
   - templates and example implementations: [references/code-examples.md](references/code-examples.md)
3. Apply the preferred top-level structure: `infrastructure / persistence / business / web`. Use `interfaces` instead of `web` when the project has multiple inbound entry types such as HTTP, MQ, scheduled jobs, and webhooks.
4. Add `integration` only when third-party integrations become large enough to deserve an independent infrastructure module.
5. Keep HTTP request objects in `web` only. Let `business` orchestrate use cases. Push strong business rules into `domain`. Keep `persistence` focused on data access.
6. Enforce naming strictly:
   - constants by category: `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`, `XxxApiPaths`, `XxxSecurityPaths`, `XxxErrorMessages`
   - enums end with `Enum`
   - API paths use short hyphen-case
   - module, package, directory, and class naming should follow the detailed rules in the reference doc
7. Put third-party integrations such as `OSS`, `TTS`, `AI`, SMS, payment, and push clients in `infrastructure/client` by default. If integrations grow large, split them into `integration/client`, but keep them inside infrastructure boundaries.
8. Keep business orchestration in `business` and callback, webhook, MQ, or job entrypoints in `web` or `interfaces`.
9. Ban magic strings and magic numbers in business code. Do not use catch-all constant classes such as `Constants` or `CommonConstants`.
10. Choose a single explicit concurrency strategy for each business chain and keep it centralized. Do not mix multiple ad hoc concurrency styles in the same workflow.
11. When Codex generates or modifies Java backend code, Chinese comments are mandatory for classes, `public` / `protected` methods, Repo methods, key business fields, and non-obvious business branches. Field comments should explain clear business meaning, units, status semantics, source, or usage boundary when the name alone is not enough.
12. For pure carrier objects such as `Request` / `Response` / `Command` / `Query` / `VO`, prefer Lombok annotations to remove boilerplate accessors. When both read and write access are needed, prefer `@Data`; when only read access is needed, prefer `@Getter`; add `@Builder` only when the object construction style truly benefits from builder semantics. For enums, default to `@Getter` only and do not add `@Setter`. Do not handwrite trivial getter/setter methods unless framework constraints or non-trivial logic make them necessary.
13. After each module is completed, regression test all APIs in that module, not only the endpoints changed in the current task.

## Reference Navigation

Read these files as needed:

- [references/architecture-and-boundaries.md](references/architecture-and-boundaries.md)
- [references/coding-standards.md](references/coding-standards.md)
- [references/security-integration-and-delivery.md](references/security-integration-and-delivery.md)
- [references/secure-baseline.md](references/secure-baseline.md)
- [references/evolution-and-governance.md](references/evolution-and-governance.md)
- [references/templates-and-checklists.md](references/templates-and-checklists.md)
- [references/code-examples.md](references/code-examples.md)
- [references/java-backend-standard.md](references/java-backend-standard.md) for quick navigation only