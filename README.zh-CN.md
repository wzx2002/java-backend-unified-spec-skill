# java-backend-unified-spec-skill

英文版说明见 [README.md](README.md)。

面向 Java 后端项目的统一规范 skill，强调模块优先架构、严格命名约束、清晰目录分层、中文注释要求、安全基线、可维护性治理、第三方接入边界，以及模块完成后的完整 API 回归。

## 包含的 Skill

- `java-backend-unified-spec`

## 规范覆盖范围

- 顶层模块默认使用 `infrastructure / persistence / business / web`
- 多入口项目使用 `interfaces`
- 第三方接入规模较大时可拆分 `integration`
- 细化目录、包名、类名命名规则
- 统一使用 `必须 / 推荐 / 可选` 规则等级
- 常量按类别命名，例如 `XxxErrorCodes`、`XxxPermissionCodes`、`XxxRiskRuleCodes`、`XxxNoRepeatKeys`、`XxxLockKeys`
- 枚举统一使用 `XxxEnum`
- 默认要求生成或修改的 Java 后端代码补齐中文注释，并强调关键字段级注释
- 提供密钥、敏感数据、上传下载、回调、发布前检查等安全基线
- 提供兼容性、模块 README、ADR、质量门禁等可维护性治理规范
- 提供模块 README / ADR / PR 自检 / 评审 / 交付上线模板
- 示例代码定位为常见参考写法，而不是强绑定某个技术栈
- 禁止魔法字符串与魔法数字
- 并发策略要求统一且集中
- 每个模块完成后要求做完整 API 回归

## 仓库结构

```text
java-backend-unified-spec-skill/
|-- README.md
|-- README.zh-CN.md
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

## 安装方式

克隆仓库后，将 skill 目录复制到本地 Codex 的 skills 目录中。

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

安装完成后重启 Codex，使 skill 能被正确发现。
