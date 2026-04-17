---
name: java-backend-unified-spec
description: Unified standard for Java backend project design, implementation, refactoring, and code review. Use when Codex needs to build or modify a Java backend that should follow module-first organization, preferred top-level module naming `infrastructure / persistence / business / web`, `interfaces` for multi-entry projects, optional `integration` for heavy third-party integrations, detailed directory and class naming rules, category-based constants such as `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`, `XxxApiPaths`, `XxxSecurityPaths`, `XxxErrorMessages`, default Chinese comments for generated or modified code, explicit concurrency strategy, and full module API regression after each module is completed.
---

# Java Backend Unified Spec

## Workflow

1. Split the work by project goal or business requirement into modules first. Do not flatten the project into one global `controller / service / repo` structure.
2. Read only the relevant sections of [references/java-backend-standard.md](references/java-backend-standard.md) before designing or editing code.
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
11. When Codex generates or modifies Java backend code, add Chinese comments by default to classes, `public` / `protected` methods, Repo methods, key business fields, and non-obvious business branches. Field comments should explain clear business meaning, units, status semantics, source, or usage boundary when the name alone is not enough. Skip noisy comments for trivial getters, setters, and obvious one-line mappings.
12. After each module is completed, regression test all APIs in that module, not only the endpoints changed in the current task.

## Reference Navigation

Read these sections in [references/java-backend-standard.md](references/java-backend-standard.md) as needed:

- `顶层模块命名与工程结构`
- `模块拆分规则`
- `分层职责与边界`
- `命名规范`
- `注释规范`
- `第三方接入规范`
- `代码示例`
- `测试与交付规范`
