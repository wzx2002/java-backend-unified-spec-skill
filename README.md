# java-backend-unified-spec-skill

Unified Java backend standards and reusable skill for module-first architecture, strict naming conventions, detailed directory rules, default Chinese comments, explicit security baselines, maintainability governance, third-party integration boundaries, and full module API regression.

## Included Skill

- `java-backend-unified-spec`

## What It Enforces

- Preferred top-level module naming: `infrastructure / persistence / business / web`
- Use `interfaces` for multi-entry projects
- Optional `integration` module for large third-party adapters
- Detailed directory, package, and class naming rules
- Clear execution levels with `必须 / 推荐 / 可选`
- Strict category-based constant naming such as `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`
- `XxxEnum` suffix for enums
- Default Chinese comments for generated or modified Java backend code, including clear field-level comments for key business fields
- Explicit secure baseline for secrets, sensitive data, uploads/downloads, callbacks, and release checks
- Explicit maintainability governance for compatibility, module README, ADR, and automated quality gates
- Reusable module README / ADR / PR checklist / review checklist / release checklist templates
- Example implementations positioned as common reference styles instead of mandatory technology choices
- No magic strings
- Explicit, centralized concurrency strategy
- Full API regression after each module is completed

## Repository Structure

```text
java-backend-unified-spec-skill/
|-- scripts/
|   `-- validate_skill_consistency.py
`-- java-backend-unified-spec/
    |-- SKILL.md
    `-- references/
        |-- java-backend-standard.md
        |-- architecture-and-boundaries.md
        |-- coding-standards.md
        |-- security-integration-and-delivery.md
        |-- secure-baseline.md
        |-- evolution-and-governance.md
        |-- templates-and-checklists.md
        `-- code-examples.md
```

## Install

Clone this repository, then copy the skill folder into your local Codex skills directory.

### Windows PowerShell

```powershell
git clone https://github.com/wzx2002/java-backend-unified-spec-skill.git
New-Item -ItemType Directory -Force "$HOME\\.codex\\skills" | Out-Null
Copy-Item ".\\java-backend-unified-spec-skill\\java-backend-unified-spec" "$HOME\\.codex\\skills\\" -Recurse -Force
```

### macOS / Linux

```bash
git clone https://github.com/wzx2002/java-backend-unified-spec-skill.git
mkdir -p ~/.codex/skills
cp -R ./java-backend-unified-spec-skill/java-backend-unified-spec ~/.codex/skills/
```

Restart Codex after installation so the skill can be discovered.

## Validation

```bash
python3 -m py_compile scripts/validate_skill_consistency.py
python3 scripts/validate_skill_consistency.py
```
