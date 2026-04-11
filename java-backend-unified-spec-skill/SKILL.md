---
name: java-backend-unified-spec
description: Unified standard for Java backend project design, implementation, refactoring, code review, default Chinese comments, and stronger code quality.
Use when Codex needs to build or modify a Java backend that should follow module-first organization, preferred top-level module naming `infrastructure / persistence / business / web`, `interfaces` for multi-entry projects, optional `integration` for heavy third-party integrations, strict naming rules, category-based constants such as `XxxErrorCodes`, `XxxPermissionCodes`, `XxxRiskRuleCodes`, `XxxNoRepeatKeys`, `XxxLockKeys`, `XxxApiPaths`, `XxxSecurityPaths`, `XxxErrorMessages`, `XxxEnum` naming for enums, no magic strings, no optimistic locking, Redis distributed locks for concurrency, default Chinese comments, stronger code quality constraints, and full module API regression after each module is completed.
---

# Java Backend Unified Spec

## 默认交付要求
1. 只要使用本 Skill 生成或修改 Java 后端代码，默认就要主动补齐中文注释，不需要等待用户额外提出“请写注释”。
2. 注释默认语言统一为中文。
3. 所有新增或修改的类、接口、枚举、注解、AOP 切面、第三方 Client 适配器，都要补充类级中文注释，说明职责、所在层、关键协作方和边界。
4. 所有新增或修改的 `public` / `protected` 方法、Repo 方法、核心领域方法，都要补充中文方法注释，说明用途、参数、返回值、异常语义、副作用，以及事务 / 锁 / 幂等 / 权限等关键约束。
5. 对于状态流转、金额处理、数据范围、分布式锁、幂等键、重试策略、验签逻辑、兼容分支、复杂 SQL 过滤条件等“不明显”的逻辑，必须补充中文行内注释，重点解释“为什么这样做”，不要只复述代码表面含义。
6. 简单 getter / setter、Lombok 注解、显而易见的一行属性映射，不要写噪音注释。
7. 修改已有代码时，必须同步补齐本次触达代码路径中的中文注释，并确保注释与实现保持一致。
8. 严禁出现占位式注释，例如：`TODO 后续处理`、`业务逻辑`、`处理数据`、`调用服务`。

## 工作流程
1. 先按项目目标或业务需求拆模块，再进入分层设计。禁止把项目整体平铺成全局 `controller / service / repo` 结构。
2. 设计或修改代码前，先阅读 [references/java-backend-standard.md](references/java-backend-standard.md)。
3. 顶层结构优先使用：`infrastructure / persistence / business / web`。
4. 如果项目存在 HTTP、MQ、定时任务、Webhook 等多入口，使用 `interfaces` 代替 `web`。
5. 当第三方接入规模足够大时，再拆分 `integration` 模块；否则默认放在 `infrastructure/client`。
6. `web / interfaces` 只处理入口适配与参数校验；`business` 负责用例编排；`domain` 负责强业务规则；`persistence` 负责数据访问；`integration` 负责第三方适配。
7. 严格执行命名规范：
   - 常量按类别命名：`XxxErrorCodes`、`XxxErrorMessages`、`XxxPermissionCodes`、`XxxRiskRuleCodes`、`XxxNoRepeatKeys`、`XxxLockKeys`、`XxxApiPaths`、`XxxSecurityPaths`
   - 枚举统一以 `Enum` 结尾
   - API 路径统一使用短横线风格
8. 第三方接入（OSS、TTS、AI、短信、支付、推送等）默认放在 `infrastructure/client`；规模很大时放到 `integration/client`，但仍属于基础设施边界。
9. 业务编排只能放在 `business`；回调、Webhook、MQ、Job 等入口放在 `web` 或 `interfaces`。
10. 业务代码禁止魔法字符串和魔法数字；禁止使用 `Constants`、`CommonConstants` 等大杂烩常量类。
11. 默认禁止乐观锁和 `version` 竞争更新；并发控制统一使用 Redis 分布式锁。
12. 每完成一个模块后，必须对该模块全部 API 做回归测试，而不是只验证本次改动接口。

## 代码质量门槛
1. 一个方法只做一个抽象层级的事情。方法同时混杂参数校验、业务编排、状态流转、SQL 细节、第三方适配时，必须拆分。
2. 优先使用卫语句和早返回，避免深层嵌套；普通业务方法默认不应超过 3 层嵌套。
3. 方法过长、分支过多、圈复杂度明显升高时，优先抽取 `XxxManager`、`XxxValidator`、`XxxPolicy`、`XxxConvert` 或私有方法。
4. `web / interfaces` 校验外部输入格式；`domain` 或 `validator` 校验业务不变量；不要把两类校验混写。
5. 事务默认放在 `business` 用例编排层，不要把事务散落在 Controller、Repo、Client 中。
6. 不要吞异常。只有在“转换异常语义、补充上下文、重试、降级、统一日志”时才允许 `catch`。
7. 列表、分页、批量查询等返回值不要返回 `null` 集合；能返回空集合就返回空集合。
8. 装配器、转换器、Mapper XML 辅助代码保持纯粹，不承载业务规则。
9. 所有日志都要保留业务关键键值和 `TraceId`（适用时），且禁止打印密码、Token、验证码、银行卡号等敏感信息。
10. 依赖注入优先使用构造器注入；依赖关系必须显式。
11. 涉及金额时统一使用 `BigDecimal`；禁止使用 `double` / `float` 做金额计算。
12. 批量数据处理时，优先避免循环内反复查库、反复调第三方接口，防止产生 N+1 查询或放大外部调用成本。
13. 新增或修改代码后，必须自检：命名是否合规、注释是否齐全、边界是否正确、异常语义是否清晰、是否存在重复逻辑、是否需要补测。

## 输出要求
1. 默认直接输出符合规范的实现，不要把“是否需要补注释”“是否需要提炼方法”留给用户二次提醒。
2. 如果用户要求的是“修改现有代码”，则除了完成目标功能，还要顺手修正触达范围内明显的命名、注释、异常处理、空值处理和分层边界问题。
3. 如果用户要求的是“设计或搭建模块”，输出的骨架代码、接口定义、示例实现、示例测试都要带中文注释。
4. 如果用户要求的是“代码评审”，要明确指出违反本 Skill 的项，并给出修正后的代码或结构建议。

## 参考导航
按需阅读 [references/java-backend-standard.md](references/java-backend-standard.md) 中这些章节：
- `顶层模块命名与工程结构`
- `模块拆分规则`
- `分层职责与边界`
- `命名规范`
- `注释规范`
- `代码质量与可维护性规范`
- `安全、权限与风控规范`
- `第三方接入规范`
- `代码示例`
- `测试与交付规范`
