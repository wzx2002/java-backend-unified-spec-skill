---
name: java-backend-unified-spec
description: Unified standard for Java backend project design, implementation, refactoring, and code review. Use when Codex needs to build or modify a Java backend that should follow module-first organization, preferred top-level module naming `infrastructure / persistence / business / web`, `interfaces` for multi-entry projects, optional `integration` for heavy third-party integrations, strict naming rules, category-based constants such as `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`, `XxxApiPaths`, `XxxSecurityPaths`, `XxxErrorMessages`, `XxxEnum` naming for enums, no magic strings, no optimistic locking, Redis distributed locks for concurrency, and full module API regression after each module is completed.
---

# Java Backend Unified Spec

## Workflow

1. Split the work by project goal or business requirement into modules first. Do not flatten the project into one global `controller / service / repo` structure.
2. Read [references/java-backend-standard.md](references/java-backend-standard.md) before designing or editing code.
3. Apply the preferred top-level structure: `infrastructure / persistence / business / web`. Use `interfaces` instead of `web` when the project has multiple inbound entry types such as HTTP, MQ, scheduled jobs, and webhooks.
4. Add `integration` only when third-party integrations become large enough to deserve an independent infrastructure module.
5. Keep HTTP request objects in `web` only. Let `business` orchestrate use cases. Push strong business rules into `domain`. Keep `persistence` focused on data access.
6. Enforce naming strictly:
   - constants by category: `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`, `XxxApiPaths`, `XxxSecurityPaths`, `XxxErrorMessages`
   - enums end with `Enum`
   - API paths use short hyphen-case
7. Put third-party integrations such as `OSS`, `TTS`, `AI`, SMS, payment, and push clients in `infrastructure/client` by default. If integrations grow large, split them into `integration/client`, but keep them inside infrastructure boundaries.
8. Keep business orchestration in `business` and callback, webhook, MQ, or job entrypoints in `web` or `interfaces`.
9. Ban magic strings and magic numbers in business code. Do not use catch-all constant classes such as `Constants` or `CommonConstants`.
10. Ban optimistic locking and `version`-based concurrency by default. Use Redis distributed locks for concurrency control.
11. After each module is completed, regression test all APIs in that module, not only the endpoints changed in the current task.

## Reference Navigation

Read these sections in [references/java-backend-standard.md](references/java-backend-standard.md) as needed:

- `顶层模块命名与工程结构`
- `模块拆分规则`
- `分层职责与边界`
- `命名规范`
- `安全、权限与风控规范`
- `第三方接入规范`
- `代码示例`
- `测试与交付规范`
