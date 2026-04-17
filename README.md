# java-backend-unified-spec-skill

Unified Java backend standards and reusable skill for module-first architecture, strict naming conventions, detailed directory rules, default Chinese comments, third-party integration boundaries, explicit concurrency strategy, and full module API regression.

## Included Skill

- `java-backend-unified-spec`

## What It Enforces

- Preferred top-level module naming: `infrastructure / persistence / business / web`
- Use `interfaces` for multi-entry projects
- Optional `integration` module for large third-party adapters
- Detailed directory, package, and class naming rules
- Strict category-based constant naming such as `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`
- `XxxEnum` suffix for enums
- Default Chinese comments for generated or modified Java backend code, including clear field-level comments for key business fields
- No magic strings
- Explicit, centralized concurrency strategy
- Full API regression after each module is completed

## Repository Structure

```text
java-backend-unified-spec-skill/
`-- java-backend-unified-spec/
    |-- SKILL.md
    `-- references/
        `-- java-backend-standard.md
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
