# Java 后端统一开发规范与示例模板

## 1. 目标

本文档作为 Java 后端项目的通用规范参考，聚焦工程结构、分层边界、命名、注释、代码质量与交付要求。

目标如下：

- 统一工程结构与顶层模块命名
- 统一分层边界与职责
- 统一命名规范与常量体系
- 统一默认中文注释标准
- 统一代码质量、自检与回归口径

## 2. 通用技术原则

本文档不强制绑定特定 JDK 版本、框架版本或基础设施选型，优先约束工程规范和实现边界。

通用原则：

- 优先沿用项目现有稳定技术栈，不要为了套规范强行升级 JDK、框架或中间件版本
- 版本选择以团队基线、生产环境约束、兼容性要求为准
- 能通过已有框架、ORM、Mapper、Client 适配层实现的能力，优先复用，不要重复造轮子
- 数据访问、接口鉴权、日志审计、缓存、消息、第三方集成等技术实现可以按项目现状落地，但必须遵守本文档的分层、命名、注释和质量约束

编码与资源要求：

- 源码、配置、SQL、XML、YAML、Properties、Markdown、脚本统一使用 `UTF-8`
- 禁止提交 `GBK`、`ANSI`、`BOM` 文件

## 3. 使用方式

使用本文档时，优先关注以下内容：

- 新项目或大改造时，先看 `顶层模块命名与工程结构`、`模块拆分规则`、`分层职责与边界`
- 日常开发或重构时，重点看 `命名规范`、`注释规范`、`代码质量与可维护性规范`
- 接入第三方、权限、日志、风控或支付等能力时，再阅读对应专题章节
- 做代码评审、自测或提测时，重点看 `测试与交付规范`

## 4. 顶层模块命名与工程结构

新项目顶层模块命名统一优先使用：

- `infrastructure`
- `persistence`
- `business`
- `web`
- `integration`，可选，仅当第三方接入很多时拆分

补充规则：

- 如果项目同时存在 HTTP、MQ、定时任务、Webhook 等多入口，`web` 升级为 `interfaces`
- `integration` 属于基础设施边界，不是业务层
- 不推荐新项目继续使用 `framework / model / service / application` 作为顶层模块名
- `business` 是顶层业务模块名，模块内部依然可以保留 `service / service/impl` 目录
- `persistence` 是顶层数据访问模块名，模块内部实体目录依然统一使用 `model`
- 如果工程实际模块名需要带项目名前缀，保持整体一致即可，例如 `order-infrastructure`、`order-persistence`

标准结构：

```text
project-parent
├─ infrastructure
├─ persistence
├─ business
├─ web
└─ integration (optional)
```

多入口项目结构：

```text
project-parent
├─ infrastructure
├─ persistence
├─ business
├─ interfaces
└─ integration (optional)
```

旧命名映射关系：

- `framework` -> `infrastructure`
- `model` -> `persistence`
- `service` -> `business`
- `application` -> `web`

## 5. 模块拆分规则

模块默认按“项目目标”或“业务需求”拆分，再在模块内部按分层结构展开。

强制规则：

- 先按业务模块拆分，再按技术层落包
- 新需求如果业务边界清晰，必须单独成模块
- 禁止把无关需求全部塞进同一个“大杂烩模块”
- 禁止只按 `controller / service / repo` 做全局平铺，不做业务模块划分
- `infrastructure` 只放基础设施能力，不承载具体业务模块
- `integration` 只放第三方接入能力，不承载具体业务规则
- `web` 或 `interfaces` 只负责入口适配，不承载核心业务规则

## 6. 分层职责与边界

### 6.1 infrastructure 层职责

负责基础设施能力：

- 基础配置
- ORM / Mapper / SQL 基础配置
- 逻辑删除全局配置
- 分页
- 防抖
- 幂等
- 锁能力封装
- 权限与数据范围基础能力
- 审计日志
- 登录日志与操作日志
- 风控
- TraceId
- JWT
- 缓存
- HTTP Client
- 全局异常

推荐目录：

```text
infrastructure
├─ config
├─ web
├─ security
├─ permission
├─ datascope
├─ audit
├─ log
├─ risk
├─ hardening
├─ mybatis
├─ trace
├─ exception
├─ exception/code
├─ response
├─ util
├─ redis
├─ lock
├─ idempotent
├─ debounce
└─ client
```

### 6.2 persistence 层职责

负责数据访问层：

- 数据库实体
- 枚举
- Mapper
- Repo
- RepoImpl
- DTO
- QueryCondition
- XML SQL

推荐目录：

```text
persistence
└─ order
   ├─ model
   ├─ enums
   ├─ mapper
   ├─ repo
   ├─ repo/impl
   ├─ dto
   ├─ query
   └─ mapper/xml
```

### 6.3 business 层职责

负责业务用例编排：

- Command
- Query
- VO
- Convert
- Service
- ServiceImpl
- Domain

推荐目录：

```text
business
└─ order
   ├─ command
   ├─ query
   ├─ vo
   ├─ convert
   ├─ service
   ├─ service/impl
   └─ domain
      ├─ manager
      ├─ validator
      └─ policy
```

### 6.4 web / interfaces 层职责

负责接口入口层：

- Controller
- Request / Response
- 参数校验
- 鉴权接入
- Assembler
- 回调、Webhook、消息消费、定时任务入口

推荐目录：

```text
web
├─ admin
│  └─ order
│     ├─ controller
│     ├─ request
│     └─ assembler
└─ api
   └─ order
      ├─ controller
      ├─ request
      └─ assembler
```

多入口项目推荐目录：

```text
interfaces
├─ http
├─ webhook
├─ mq
└─ job
```

### 6.5 integration 层职责

仅在第三方接入特别多时拆分，负责：

- 三方 Client 聚合
- 厂商配置与鉴权
- 回调验签与请求签名
- SDK 适配与容错封装
- 共享第三方模板能力

禁止：

- 业务规则编排
- 业务状态流转
- Controller / Request / Response
- 直接承载业务权限判断

推荐目录：

```text
integration
└─ client
   ├─ oss
   │  ├─ OssClient.java
   │  ├─ OssProperties.java
   │  └─ XxxOssClient.java
   ├─ tts
   │  ├─ TtsClient.java
   │  ├─ TtsProperties.java
   │  └─ XxxTtsClient.java
   └─ ai
      ├─ AiClient.java
      ├─ AiProperties.java
      └─ XxxAiClient.java
```

### 6.6 边界强制规则

`web / interfaces` 只负责：

- 接收请求
- 参数校验
- 调用 Assembler
- 调用 Business Service
- 返回统一响应

`web / interfaces` 禁止：

- 写 SQL
- 写金额计算
- 写状态机
- 写数据范围拼装
- 直接调用 Mapper
- 直接调用厂商 SDK

`business` 只负责：

- 用例编排
- 事务控制
- 跨聚合协同
- 调 Repo
- 调 Domain
- 调 Convert
- 决定是否调用第三方 Client

`business` 禁止：

- 直接写 SQL
- 直接调 Mapper
- 直接散写错误码、权限码、锁 key、操作名称等业务字面量
- 直接写厂商 SDK 初始化、签名和底层重试逻辑

`domain` 负责：

- 状态机
- 金额规则
- 不变量校验
- 聚合内规则封装

`domain` 建议至少具备：

- `XxxManager`
- `XxxValidator`
- `XxxPolicy`

`persistence` 只负责：

- 单表简单查询
- 单表状态更新
- XML 查询代理

`persistence` 统一规则：

- 单表简单查询优先使用项目既有 ORM / Mapper 查询能力
- 单表状态更新优先使用项目既有数据访问组件能力
- 多表联查、统计、导出、对账统一进入明确的数据访问实现，例如 SQL 文件、Mapper XML 或查询实现类
- Repo 查询方法必须写中文注释

`integration` 或 `infrastructure/client` 只负责：

- SDK 初始化与配置
- 鉴权、签名、验签
- 超时、重试、容错封装
- 第三方异常映射

`integration` 或 `infrastructure/client` 禁止：

- 业务规则判断
- 直接拼装 Controller Request / Response
- 直接承载业务状态流转

## 7. 命名规范

### 7.1 目录与包命名

- 实体目录统一使用 `model`
- 禁止使用 `do` 作为目录名
- 枚举统一放 `enums`
- XML 统一放 `resources/mapper/**`
- 顶层模块统一使用 `infrastructure`、`persistence`、`business`、`web`
- 多入口项目把 `web` 升级为 `interfaces`
- 第三方接入规模不大时统一放 `infrastructure/client`；规模明显扩大后再拆 `integration/client`
- 包路径优先按 `层 + 业务模块` 组织，不要只按技术类型全局平铺
- `web` / `interfaces` 推荐按入口域拆目录，例如 `admin/order/controller`、`api/order/request`、`mq/order/consumer`
- `business` 推荐按业务模块拆目录，例如 `order/command`、`order/query`、`order/service`、`order/domain`
- `domain` 下优先使用 `manager`、`validator`、`policy` 表达业务规则角色，不要堆在一个 `service` 包里
- `persistence` 推荐按业务模块拆目录，例如 `order/model`、`order/repo`、`order/mapper`、`order/query`
- 包名、目录名统一使用小写英文语义词，避免 `common`、`util2`、`temp`、`misc` 这类无业务语义命名
- 同一业务模块下，目录层级优先保持稳定，不要同一处同时出现 `dto`、`param`、`request` 三套近义目录
- Web 入参统一使用 `request`，出参优先使用 `response` 或直接复用 `VO` 规则，内部编排输入统一使用 `command` / `query`
- 能表达业务边界时，目录名优先用完整业务词，如 `settlement`、`reconciliation`、`withdraw`，不要只写模糊缩写

### 7.2 类命名

- 实体类：`XxxDO`
- 枚举类：`XxxEnum`
- Mapper：`XxxMapper`
- 仓储接口：`XxxRepo`
- 仓储实现：`XxxRepoImpl`
- 命令对象：`XxxCommand`
- 查询对象：`XxxQuery`
- 视图对象：`XxxVO`
- 转换器：`XxxConvert`
- 服务接口：`XxxService`
- 服务实现：`XxxServiceImpl`
- Web 装配器：`XxxWebAssembler`
- 领域管理器：`XxxManager`
- 规则校验器：`XxxValidator`
- 业务策略：`XxxPolicy`

### 7.3 接口路径

- 后台接口统一 `/admin/**`
- 前台接口统一 `/api/**`
- 路径统一使用短横线风格，如 `/confirm-order`
- 禁止接口路径使用驼峰命名

### 7.4 常量类命名

禁止出现魔法字符串和魔法数字。常量类统一按类别命名，不要把所有内容塞进 `Constants`：

- 错误码：`XxxErrorCodes`
- 错误消息：`XxxErrorMessages`
- 权限码：`XxxPermissionCodes`
- 风控规则码：`XxxRiskRuleCodes`
- 分布式锁 Key：`XxxLockKeys`
- 防重复提交 Key：`XxxNoRepeatKeys`
- API 路径：`XxxApiPaths`
- 安全路径：`XxxSecurityPaths`

禁止命名：

- `Constants`
- `CommonConstants`
- `Const`
- `ConfigConst`
- `OrderConstant`
- `SystemConstant`

### 7.5 常量字段命名

常量字段统一使用 `UPPER_SNAKE_CASE`。

补充规则：

- 锁 Key 前缀常量统一以 `_PREFIX` 结尾
- 路径常量优先用语义命名，如 `ADMIN_BASE`、`CONFIRM_ORDER`
- 正则或路径匹配常量优先以 `_PATTERN` 结尾

### 7.6 常量值格式

- 错误码值：`UPPER_SNAKE_CASE`
- 权限码值：`lower-hyphen-case`
- 防重复 Key 值：`lower:colon:case`
- 锁 Key 前缀值：`lower:colon:case`
- 接口路径值：`/segment-name`
- 安全匹配值：`/segment/**`

### 7.7 常量类实现规则

常量类必须满足：

- 使用 `final class`
- 提供私有构造方法
- 不允许实例化
- 不允许把多个类别混在同一个类里
- 可以提供少量 Key 拼装方法，但方法名必须是完整业务语义

### 7.8 枚举命名

- 枚举类统一使用 `XxxEnum` 结尾
- 枚举项统一使用 `UPPER_SNAKE_CASE`
- 状态、类型、来源、原因等有限取值判断，优先收口到枚举静态方法，例如 `OrderStatusEnum.isPending(status)`
- 不要在业务代码中重复散写 `XxxEnum.SOME_STATUS.getCode().equals(value)` 这类判断

## 8. 注释规范

### 8.1 默认要求

- AI 生成或修改代码时，默认主动补齐中文注释，不需要等待用户单独提出
- 注释默认语言统一为中文
- 注释必须服务于“可维护性”和“业务可读性”，不要写成噪音
- 对关键业务字段，默认要补齐字段级中文注释，且注释语义要清晰到足以支撑维护、联调和评审

### 8.2 类级注释

以下类型默认必须写类级中文注释：

- 业务 Service / ServiceImpl
- Domain Manager / Validator / Policy
- Repo / RepoImpl
- Controller / Assembler
- 自定义注解与 AOP 切面
- 第三方 Client / Properties / Adapter
- 自定义异常、统一响应、全局异常处理类
- 关键枚举、重要常量类

类级注释至少说明：

- 当前类职责
- 所在分层
- 关键协作对象
- 边界约束或注意事项

类可以按需要使用注解，例如 `@Builder`、`@Getter`、`@Setter`、`@Data`、`@NoArgsConstructor`、`@AllArgsConstructor`、`@Slf4j`、`@Service`、`@Component`、`@Configuration` 等，但注解不能替代类注释本身，也不能替代关键字段和关键方法的语义说明。

### 8.3 方法注释

以下方法默认必须写中文方法注释：

- `public` / `protected` 方法
- Repo 查询方法和状态更新方法
- Domain 核心规则方法
- 第三方调用适配方法
- 涉及事务、分布式锁、幂等、防抖、权限、审计、风控的方法

方法注释建议包含：

- 方法用途
- 参数语义
- 返回值语义
- 可能抛出的业务异常
- 事务、锁、重试、回调、副作用等约束

### 8.4 字段注释

以下字段建议补充中文注释：

- 业务语义不直观的领域字段
- 金额、状态、来源、原因等关键字段
- 锁 Key 前缀、权限码、风控规则码、错误码、错误消息
- 第三方配置项、签名字段、回调验签字段

字段注释要优先说明以下信息中的一项或多项：

- 字段业务含义，而不只是字面翻译
- 金额单位、比例口径、是否含税、是否允许负数
- 状态字段的取值语义、流转阶段、前后置条件
- 来源字段的生成方式、同步来源、回填来源
- 标识字段的唯一性口径、关联对象、使用边界
- 时间字段的时区语义、业务时点、系统时点

简单 DTO / VO 中名称非常直观的字段可不重复写注释，但只要字段承担状态、金额、权限、风控、外部映射、兼容分支等关键语义，就必须写清楚。

#### 8.4.1 字段注释示例

推荐写法示例：

```java
public class OrderDO {

    /**
     * 订单确认状态。
     * 仅允许使用 {@link OrderConfirmStatusEnum} 中定义的状态值。
     *
     * @see OrderConfirmStatusEnum
     */
    private Integer confirmStatus;

    /**
     * 订单应付金额，单位为元，含两位小数。
     * 该金额为用户侧应付口径，已包含优惠抵扣，不允许为负数。
     */
    private BigDecimal payableAmount;

    /**
     * 订单来源渠道。
     * 该字段记录订单首次创建来源，例如后台录单、用户自主下单、第三方平台导入。
     */
    private String sourceType;

    /**
     * 外部支付流水号。
     * 该值由支付渠道回调返回，用于关联渠道侧支付结果与本地支付单。
     */
    private String externalPayNo;

    /**
     * 业务完成时间。
     * 使用业务事件实际完成时点，不等同于记录更新时间。
     */
    private LocalDateTime completedAt;
}
```

不推荐写法示例：

```java
public class OrderDO {

    /** 确认状态 */
    private Integer confirmStatus;

    /** 金额 */
    private BigDecimal payableAmount;

    /** 来源 */
    private String sourceType;
}
```

判断标准：

- 好的字段注释要回答“这个字段在业务上到底代表什么”
- 如果字段存在枚举值、金额口径、状态前置条件、外部来源、时区语义，注释中应直接写出来
- 状态、类型、来源、原因、渠道等有限取值字段，优先抽成 `XxxEnum`，字段注释通过 `@see` 或 `{@link ...}` 指向对应枚举
- 注释不能只把字段名翻译成中文，否则对维护、联调和评审帮助很弱

#### 8.4.2 注解与字段注释配合示例

```java
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderCreateResultVO {

    /**
     * 订单确认状态。
     * 仅允许使用 {@link OrderConfirmStatusEnum} 中定义的状态值。
     *
     * @see OrderConfirmStatusEnum
     */
    private Integer confirmStatus;

    /**
     * 订单应付金额，单位为元，含两位小数。
     */
    private BigDecimal payableAmount;
}
```

约束说明：

- `@Builder`、`@Getter`、`@Setter` 等注解可以正常使用
- 注解用于减少样板代码，不承担业务语义表达职责
- 只要字段本身承载关键业务语义，仍然要写清晰的字段注释

### 8.5 行内注释

行内注释只写“为什么”，重点覆盖：

- 状态机与状态流转前置条件
- 金额口径与精度处理
- 数据范围收敛点
- 分布式锁粒度与锁键拼装依据
- 幂等键选择依据
- 事务边界与补偿点
- 验签、重试、降级、兼容分支
- 复杂 SQL 条件、排序、分页口径

### 8.6 禁止事项

禁止以下注释：

- 只复述代码字面含义
- 与实现不一致的过期注释
- `TODO 后续处理`、`业务逻辑`、`处理数据` 这类空泛注释
- 大段注释掉的旧代码
- 中英文混杂但缺乏统一规范的注释

### 8.7 修改代码时的要求

- 只要修改了某个类或方法，就要同步检查并补齐其中文注释
- 代码重构后必须同步更新注释，禁止保留旧语义注释
- 评审时把“注释是否覆盖关键语义”作为必查项

## 9. 数据库规范

业务表默认字段：

- `created_at`
- `updated_at`
- `is_deleted`
- `deleted_at`

建议补齐：

- `created_by`
- `updated_by`

统一规则：

- 逻辑删除统一走全局配置
- 唯一索引必须把 `is_deleted` 纳入唯一键
- 数据库字符集统一 `utf8mb4`
- 索引围绕查询条件、排序字段、唯一约束设计
- 禁止把数据范围配置成 SQL 字符串片段

## 10. 安全、权限与风控规范

### 10.1 JWT 鉴权

- `/api/**` 只接受前台 Token
- `/admin/**` 只接受后台 Token
- 前后台必须使用两套 `SecurityFilterChain`
- 匿名放行接口仅限 `login / register / send-sms / refresh-token`
- `logout`、`me`、资料修改、业务查询等接口必须要求有效 Access Token
- 前后台 Token 必须区分 `tokenType`、`issuer`、`audience`
- 前后台缓存、黑名单、Refresh Token 命名空间必须隔离

### 10.2 长期登录

- 不允许超长 Access Token 直接长期登录
- 必须采用 `短效 access token + 长效 refresh token`
- Refresh Token 必须可控、可吊销、可失效、可审计
- Logout 时至少吊销当前操作人的 Refresh Token

### 10.3 五层权限模型

统一采用：

- 模块权限
- 动作权限
- 字段权限
- 数据范围
- 敏感动作权限

强制规则：

- 不能只在前端做权限控制
- 列表、详情、导出、统计必须复用同一套数据范围规则
- 数据范围必须落在 Query 构造或 Repo 入口
- 敏感字段脱敏必须在后端完成
- 查看敏感字段明文必须单独授权并写审计日志

### 10.4 防抖、幂等、并发控制

适用场景：

- 发送验证码
- 注册
- 生成订单
- 提现申请
- 审核动作
- 打款动作
- 支付回调
- 第三方重试回调
- 财务确认与冲销

强制规则：

- 并发控制策略必须在项目内统一，不要在同一业务链路中混用多套并发方案
- 可以根据项目现状选择分布式锁、数据库锁、唯一约束、乐观锁或其他成熟方案，但要明确适用边界
- 并发控制组件统一放 `infrastructure`
- 并发控制使用位置统一在 `business` 或 `domain manager`
- 如果使用锁方案，优先提供闭包式执行接口，如 `executeWithLock(...)`
- 并发获取失败或并发冲突时统一抛出语义明确的异常，不允许静默吞掉
- 并发控制键、条件或约束必须稳定、可预测、可审计

### 10.5 日志与审计

必须具备：

- 登录日志
- 操作日志
- 审计日志
- 风控日志
- TraceId

推荐能力：

- `@OperationLog`
- `@SensitiveOperationLog`
- `@RiskCheck`
- `@PermissionCheck`
- `@NoRepeatSubmit`

## 11. 异常、日志与响应规范

统一原则：

- 所有接口异常统一由 `GlobalExceptionHandler` 收口
- 不允许每个 Controller 单独写大段 `try/catch`
- 异常分类必须明确
- 前后台统一使用同一套响应结构
- 统一响应优先使用带泛型的响应体，例如 `CommonResponse<T>`，不要到处使用原始类型
- 参数前置校验统一优先使用 Apache Commons Lang3 的 `Validate.notNull(...)`、`Validate.isTrue(...)` 等写法，不要在业务代码中散写重复的 `if (...) { throw ... }`

推荐异常类：

- `BizException`
- `PermissionException`
- `DataScopeException`
- `RiskControlException`
- `ThirdPartyCallbackException`
- `FileUploadException`
- `FinanceException`

日志要求：

- `BizException` 默认按 `warn` 级别记录
- 数据库异常、未知运行时异常默认按 `error` 级别记录
- 日志必须带 `TraceId`
- 禁止打印密码、Token、验证码、银行卡号等敏感信息

异常处理细则：

- 不要直接抛裸 `RuntimeException`
- `catch` 后如重新抛出，必须补充上下文语义
- 第三方异常要映射成业务可理解的异常类型
- Controller 只负责抛出语义明确的异常，不负责拼装复杂错误响应
- `Validate` 触发的参数校验异常要由统一异常处理器收口
- 不要把所有 `NullPointerException` 一律映射为参数错误，避免把真实程序错误误判成前置校验失败

## 12. 代码质量与可维护性规范

### 12.1 单一职责与抽象层级

- 一个类尽量聚焦一个主要职责
- 一个方法只做一个抽象层级的事情
- 当一个方法同时混杂“参数校验 + 业务编排 + 状态流转 + 持久化细节 + 第三方调用”时，必须拆分

### 12.2 方法体控制

- 优先使用卫语句和早返回，降低嵌套深度
- 普通业务方法默认不应超过 3 层嵌套
- 方法过长、分支过多、可读性下降时，优先抽私有方法或专用组件
- 复杂业务优先抽取 `XxxManager`、`XxxValidator`、`XxxPolicy`

### 12.3 空值与返回值

- 列表、分页、批量结果默认不返回 `null`
- 查无数据时优先返回空集合、空页对象或显式业务异常
- 不要把 `null` 当成跨层协议的常规语义

### 12.4 校验分层

- `web / interfaces` 负责格式校验、必填校验、长度校验、枚举值校验
- `domain` 或 `validator` 负责业务不变量、状态合法性、金额口径校验
- `business`、`domain`、`validator` 中的前置条件校验，优先统一使用 `org.apache.commons.lang3.Validate`
- 对空值校验统一优先使用 `Validate.notNull(...)`
- 对布尔条件校验统一优先使用 `Validate.isTrue(...)`
- 不要在多个业务方法里重复散写 `if (...) { throw new BizException(...) }` 作为基础前置校验模板
- Repo 不承载业务规则校验

### 12.5 事务与一致性

- 事务默认放在 `business` 编排层
- 不要把事务散落在 Controller、Repo、Client
- 涉及资金链路、状态流转、流水写入时，要明确事务边界和补偿策略
- 涉及回调幂等时，要显式说明幂等键来源

### 12.6 异常处理质量

- 不允许吞异常
- 只有在“转换异常语义、补充上下文、重试、降级、日志增强”时才允许 `catch`
- 业务异常与系统异常必须区分清楚
- 不要把所有异常都映射成同一个模糊错误码

### 12.7 查询与性能

- 批量处理优先批量查库、批量写库，避免循环内查库形成 N+1
- 多表联查、统计、导出、对账统一进入 XML
- 分页查询必须保证排序口径明确
- 对高频接口明确缓存、锁、幂等或防抖策略

### 12.8 可读性与可评审性

- 常量、枚举、异常、响应结构要语义清晰
- 不允许散写业务字面量
- 装配器与转换器保持纯粹，不写业务规则
- 重要类、方法、关键分支必须带中文注释
- 代码提交前至少完成一次“命名 / 注释 / 边界 / 异常 / 空值 / 重复逻辑”自检

### 12.9 金额与时间

- 金额统一使用 `BigDecimal`
- 禁止使用 `double` / `float` 做金额计算
- 时间语义统一使用明确类型，如 `LocalDateTime`、`LocalDate`
- 不要跨层用裸字符串承载复杂时间语义

## 13. 第三方接入规范

统一规则：

- `OSS`、`TTS`、`AI`、短信、支付、推送等 SDK 默认放 `infrastructure/client`
- 当三方接入特别多时，拆 `integration` 模块，目录统一放 `integration/client`
- `infrastructure/client` 或 `integration/client` 只负责厂商配置、鉴权、签名、SDK 适配、超时、重试、异常映射
- 第三方回调接口、Webhook、异步通知入口统一放 `web`，多入口项目统一放 `interfaces`
- 是否调用三方、何时调用、调用结果如何回写业务数据，统一由 `business` 编排
- `domain` 禁止直接依赖厂商 SDK
- 第三方调用记录、任务表、结果表放对应业务模块的 `persistence`

推荐目录：

```text
infrastructure
└─ client
   ├─ oss
   ├─ tts
   └─ ai
```

或：

```text
integration
└─ client
   ├─ oss
   ├─ tts
   └─ ai
```

## 14. 财务项目附加规则

只要项目涉及资金链路，额外强制：

- 金额真实来源只认事实表
- 已确认记录禁止直接改金额，只能冲销
- 确认、冲销、付款、发放接口必须幂等
- 有天然业务单号的动作直接以业务单号做幂等键
- 无天然业务单号的动作必须显式传 `requestNo`
- 资金流水必须与确认动作同事务落库
- 审计日志必须记录前值、后值、原因、`TraceId`
- 对账必须能校验事实表与资金流水一致

## 15. 类模板清单

### 15.1 infrastructure 层最少应具备

```text
infrastructure
├─ security
│  ├─ FrontSecurityConfig.java
│  ├─ AdminSecurityConfig.java
│  ├─ JwtTokenService.java
│  ├─ FrontJwtAuthenticationFilter.java
│  └─ AdminJwtAuthenticationFilter.java
├─ mybatis
│  ├─ MybatisPlusConfig.java
│  └─ CommonMetaObjectHandler.java
├─ lock
│  ├─ DistributedLockExecutor.java
│  └─ RedisDistributedLockExecutor.java
├─ debounce
│  ├─ NoRepeatSubmit.java
│  └─ NoRepeatSubmitAspect.java
├─ permission
│  ├─ PermissionCheck.java
│  └─ PermissionCheckAspect.java
├─ log
│  ├─ OperationLog.java
│  ├─ SensitiveOperationLog.java
│  └─ OperationLogAspect.java
├─ risk
│  ├─ RiskCheck.java
│  └─ RiskCheckAspect.java
├─ exception
│  ├─ BizException.java
│  ├─ PermissionException.java
│  ├─ RiskControlException.java
│  └─ GlobalExceptionHandler.java
├─ response
│  └─ CommonResponse.java
└─ client
   └─ ai
      ├─ AiClient.java
      ├─ AiProperties.java
      └─ XxxAiClient.java
```

### 15.2 persistence 层最少应具备

```text
persistence
└─ order
   ├─ model
   │  └─ OrderDO.java
   ├─ enums
   │  └─ OrderStatusEnum.java
   ├─ mapper
   │  ├─ OrderMapper.java
   │  └─ OrderQueryMapper.java
   ├─ repo
   │  └─ OrderRepo.java
   ├─ repo/impl
   │  └─ OrderRepoImpl.java
   └─ mapper/xml
      └─ OrderQueryMapper.xml
```

### 15.3 business 层最少应具备

```text
business
└─ order
   ├─ command
   │  └─ ConfirmOrderCommand.java
   ├─ query
   │  └─ OrderPageQuery.java
   ├─ vo
   │  └─ OrderVO.java
   ├─ convert
   │  └─ OrderConvert.java
   ├─ service
   │  └─ OrderService.java
   ├─ service/impl
   │  └─ OrderServiceImpl.java
   ├─ constant
   │  ├─ OrderErrorCodes.java
   │  ├─ OrderErrorMessages.java
   │  ├─ OrderPermissionCodes.java
   │  ├─ OrderRiskRuleCodes.java
   │  ├─ OrderLockKeys.java
   │  └─ OrderNoRepeatKeys.java
   └─ domain
      ├─ manager
      │  └─ OrderManager.java
      ├─ validator
      │  └─ OrderValidator.java
      └─ policy
         └─ OrderPolicy.java
```

### 15.4 web / interfaces 层最少应具备

```text
web
└─ admin
   └─ order
      ├─ controller
      │  └─ AdminOrderController.java
      ├─ request
      │  └─ ConfirmOrderRequest.java
      └─ assembler
         └─ AdminOrderWebAssembler.java
```

### 15.5 integration 层最少应具备

```text
integration
└─ client
   ├─ oss
   │  ├─ OssClient.java
   │  ├─ OssProperties.java
   │  └─ XxxOssClient.java
   ├─ tts
   │  ├─ TtsClient.java
   │  ├─ TtsProperties.java
   │  └─ XxxTtsClient.java
   └─ ai
      ├─ AiClient.java
      ├─ AiProperties.java
      └─ XxxAiClient.java
```

## 16. 单流程标准写法

以“后台确认完单”为例，标准链路如下：

1. `web` 接收请求并完成参数校验。
2. `web` 通过 Assembler 转成 `business` Command。
3. `business` 统一处理权限、防抖、日志、事务。
4. `business` 在业务主键维度执行统一并发控制策略，例如分布式锁。
5. `business` 调用 `persistence` 查询数据。
6. `domain` 校验状态并处理状态流转。
7. `persistence` 使用项目既有数据访问组件落库。
8. AOP 或事件统一记录日志、审计和风控信息。

## 17. 代码示例

以下示例只展示一种可参考实现风格，不构成对特定框架、中间件或 ORM 的强制绑定。

### 17.1 基础实体示例

```java
/**
 * 业务基础实体。
 * <p>
 * 统一沉淀审计字段和逻辑删除字段，供各业务实体继承。
 */
public class BaseDO {

    /**
     * 创建时间。
     */
    private LocalDateTime createdAt;

    /**
     * 更新时间。
     */
    private LocalDateTime updatedAt;

    /**
     * 创建人。
     */
    private Long createdBy;

    /**
     * 更新人。
     */
    private Long updatedBy;

    /**
     * 逻辑删除标记。
     */
    private Integer isDeleted;

    /**
     * 删除时间。
     */
    private LocalDateTime deletedAt;
}
```

### 17.2 常量与枚举示例

```java
/**
 * 订单业务错误码常量。
 */
public final class OrderErrorCodes {

    /**
     * 订单不存在。
     */
    public static final String ORDER_NOT_FOUND = "ORDER_NOT_FOUND";

    /**
     * 订单状态不允许确认。
     */
    public static final String ORDER_STATUS_INVALID = "ORDER_STATUS_INVALID";

    private OrderErrorCodes() {
    }
}
```

```java
/**
 * 订单业务错误消息常量。
 */
public final class OrderErrorMessages {

    /**
     * 订单不存在。
     */
    public static final String ORDER_NOT_FOUND = "订单不存在";

    /**
     * 当前订单状态不允许确认。
     */
    public static final String ORDER_STATUS_INVALID = "订单状态不允许确认";

    private OrderErrorMessages() {
    }
}
```

```java
/**
 * 订单权限码常量。
 */
public final class OrderPermissionCodes {

    /**
     * 后台确认订单权限。
     */
    public static final String ADMIN_ORDER_CONFIRM = "admin-order-confirm";

    private OrderPermissionCodes() {
    }
}
```

```java
/**
 * 订单风控规则码常量。
 */
public final class OrderRiskRuleCodes {

    /**
     * 订单确认风控规则。
     */
    public static final String ORDER_CONFIRM_AUDIT = "ORDER_CONFIRM_AUDIT";

    private OrderRiskRuleCodes() {
    }
}
```

```java
/**
 * 订单防重复提交 Key 常量。
 */
public final class OrderNoRepeatKeys {

    /**
     * 后台确认订单防重 Key 前缀。
     */
    public static final String ADMIN_ORDER_CONFIRM = "admin:order:confirm";

    private OrderNoRepeatKeys() {
    }
}
```

```java
/**
 * 订单分布式锁 Key 常量。
 */
public final class OrderLockKeys {

    /**
     * 确认订单锁前缀。
     */
    public static final String CONFIRM_ORDER_PREFIX = "order:confirm:";

    private OrderLockKeys() {
    }

    /**
     * 构造确认订单锁 Key。
     *
     * @param orderNo 订单号
     * @return 分布式锁 Key
     */
    public static String confirmOrder(String orderNo) {
        return CONFIRM_ORDER_PREFIX + orderNo;
    }
}
```

```java
/**
 * 订单接口路径常量。
 */
public final class OrderApiPaths {

    /**
     * 后台订单基础路径。
     */
    public static final String ADMIN_BASE = "/admin/order";

    /**
     * 后台确认订单路径。
     */
    public static final String CONFIRM_ORDER = "/confirm-order";

    private OrderApiPaths() {
    }
}
```

```java
/**
 * 订单状态枚举。
 */
@Getter
@RequiredArgsConstructor
public enum OrderStatusEnum {

    /**
     * 待处理。
     */
    PENDING(1, "待处理"),

    /**
     * 已确认。
     */
    CONFIRMED(2, "已确认"),

    /**
     * 已拒绝。
     */
    REJECTED(3, "已拒绝");

    private final Integer code;
    private final String description;

    /**
     * 判断是否为待处理状态。
     *
     * @param code 状态编码
     * @return 是否为待处理
     */
    public static boolean isPending(Integer code) {
        return PENDING.getCode().equals(code);
    }
}
```

### 17.3 Controller / Request / Assembler 示例

```java
/**
 * 后台订单管理控制器。
 * <p>
 * 只负责请求接收、参数校验、命令装配和统一响应，不直接承载业务规则。
 */
@RestController
@Validated
@RequiredArgsConstructor
@RequestMapping(OrderApiPaths.ADMIN_BASE)
public class AdminOrderController {

    private final OrderService orderService;
    private final AdminOrderWebAssembler adminOrderWebAssembler;

    /**
     * 后台确认订单。
     *
     * @param request 确认订单请求
     * @return 通用成功响应
     */
    @PostMapping(OrderApiPaths.CONFIRM_ORDER)
    public CommonResponse<Void> confirmOrder(@Valid @RequestBody ConfirmOrderRequest request) {
        ConfirmOrderCommand command = adminOrderWebAssembler.toConfirmOrderCommand(request);
        orderService.confirmOrder(command);
        return CommonResponse.success();
    }
}
```

```java
/**
 * 后台确认订单请求参数。
 */
@Getter
@Setter
public class ConfirmOrderRequest {

    /**
     * 订单号。
     */
    @NotBlank(message = "订单号不能为空")
    private String orderNo;

    /**
     * 确认备注。
     */
    @Size(max = 200, message = "备注长度不能超过 200")
    private String remark;
}
```

```java
/**
 * 后台订单 Web 装配器。
 * <p>
 * 负责将入口层请求对象转换为业务层命令对象，不承载业务规则。
 */
@Component
public class AdminOrderWebAssembler {

    /**
     * 将确认订单请求转换为业务命令。
     *
     * @param request 请求对象
     * @return 确认订单命令
     */
    public ConfirmOrderCommand toConfirmOrderCommand(ConfirmOrderRequest request) {
        return ConfirmOrderCommand.builder()
            .orderNo(request.getOrderNo())
            .remark(request.getRemark())
            .build();
    }
}
```

### 17.4 Command / Service / Domain 示例

```java
/**
 * 确认订单命令。
 */
@Getter
@Builder
public class ConfirmOrderCommand {

    /**
     * 订单号。
     */
    private final String orderNo;

    /**
     * 确认备注。
     */
    private final String remark;
}
```

```java
/**
 * 订单业务服务。
 */
public interface OrderService {

    /**
     * 确认订单。
     *
     * @param command 确认订单命令
     */
    void confirmOrder(ConfirmOrderCommand command);
}
```

```java
/**
 * 订单领域管理器。
 * <p>
 * 负责封装订单聚合内的状态校验和状态流转规则。
 */
@Component
public class OrderManager {

    /**
     * 校验订单是否允许确认。
     *
     * @param orderDO 订单实体
     */
    public void validateCanConfirm(OrderDO orderDO) {
        Validate.isTrue(
            OrderStatusEnum.isPending(orderDO.getStatus()),
            OrderErrorMessages.ORDER_STATUS_INVALID
        );
    }
}
```

### 17.5 ServiceImpl 示例

```java
/**
 * 订单业务服务实现。
 * <p>
 * 负责后台确认订单用例的统一编排，包括权限、防重、事务和分布式锁控制。
 */
@Service
@RequiredArgsConstructor
public class OrderServiceImpl implements OrderService {

    private final OrderRepo orderRepo;
    private final OrderManager orderManager;
    private final DistributedLockExecutor distributedLockExecutor;

    /**
     * 确认订单。
     *
     * @param command 确认订单命令
     */
    @Override
    @PermissionCheck(code = OrderPermissionCodes.ADMIN_ORDER_CONFIRM, dataScope = true)
    @NoRepeatSubmit(keyPrefix = OrderNoRepeatKeys.ADMIN_ORDER_CONFIRM, expireSeconds = 5)
    @Transactional(rollbackFor = Exception.class)
    public void confirmOrder(ConfirmOrderCommand command) {
        distributedLockExecutor.executeWithLock(
            OrderLockKeys.confirmOrder(command.getOrderNo()),
            3000L,
            10000L,
            () -> {
                // 先按业务主键查询订单，确保后续状态校验和落库都围绕同一订单展开。
                OrderDO orderDO = orderRepo.findByOrderNo(command.getOrderNo());
                Validate.notNull(orderDO, OrderErrorMessages.ORDER_NOT_FOUND);

                // 状态流转前先做领域校验，避免非法状态重复确认。
                orderManager.validateCanConfirm(orderDO);

                // 在持有分布式锁期间完成状态更新，防止并发确认造成重复写入。
                orderRepo.confirmOrder(
                    orderDO.getId(),
                    command.getRemark(),
                    OrderStatusEnum.CONFIRMED.getCode()
                );
            }
        );
    }
}
```

### 17.6 Repo / RepoImpl / XML 示例

```java
/**
 * 订单仓储接口。
 */
public interface OrderRepo {

    /**
     * 根据订单号查询订单。
     *
     * @param orderNo 订单号
     * @return 订单实体，查无数据时返回 null
     */
    OrderDO findByOrderNo(String orderNo);

    /**
     * 确认订单状态。
     *
     * @param id 订单主键
     * @param remark 确认备注
     * @param status 目标状态
     */
    void confirmOrder(Long id, String remark, Integer status);
}
```

```java
/**
 * 订单仓储实现。
 * <p>
 * 负责订单数据访问，不承载业务规则。
 */
@Repository
@RequiredArgsConstructor
public class OrderRepoImpl implements OrderRepo {

    private final OrderMapper orderMapper;

    /**
     * 根据订单号查询订单。
     *
     * @param orderNo 订单号
     * @return 订单实体，查无数据时返回 null
     */
    @Override
    public OrderDO findByOrderNo(String orderNo) {
        return orderMapper.selectOne(
            Wrappers.lambdaQuery(OrderDO.class)
                .eq(OrderDO::getOrderNo, orderNo)
        );
    }

    /**
     * 确认订单状态。
     *
     * @param id 订单主键
     * @param remark 确认备注
     * @param status 目标状态
     */
    @Override
    public void confirmOrder(Long id, String remark, Integer status) {
        orderMapper.update(
            null,
            Wrappers.lambdaUpdate(OrderDO.class)
                .eq(OrderDO::getId, id)
                .set(OrderDO::getStatus, status)
                .set(OrderDO::getConfirmRemark, remark)
        );
    }
}
```

```xml
<!--
  订单列表查询。
  说明：
  1. 仅用于复杂多表联查；
  2. 排序口径固定为主键倒序；
  3. 查询条件中的状态字段由业务层明确传入。
-->
<select id="selectOrderPage" resultType="com.example.order.dto.OrderPageDTO">
    SELECT
        o.id,
        o.order_no,
        o.status,
        u.nickname AS user_name
    FROM biz_order o
    LEFT JOIN biz_user u ON u.id = o.user_id
    WHERE o.status = #{status}
    ORDER BY o.id DESC
</select>
```

### 17.7 第三方 Client 示例

```java
/**
 * AI 能力客户端。
 */
public interface AiClient {

    /**
     * 调用 AI 聊天能力。
     *
     * @param prompt 提示词
     * @return 厂商返回文本
     */
    String chat(String prompt);
}
```

```java
/**
 * 某厂商 AI Client 适配实现。
 * <p>
 * 这里只做厂商请求封装，不承载业务规则。
 */
@Component
@RequiredArgsConstructor
public class XxxAiClient implements AiClient {

    private final AiProperties aiProperties;

    /**
     * 调用厂商 AI 接口。
     *
     * @param prompt 提示词
     * @return 厂商返回文本
     */
    @Override
    public String chat(String prompt) {
        // 这里只做厂商请求封装，不写业务规则。
        return "mock-response";
    }
}
```

### 17.8 全局异常处理示例

```java
/**
 * 全局异常处理器。
 * <p>
 * 统一收口接口异常并返回标准响应结构。
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 处理请求参数校验异常。
     *
     * @param exception 参数校验异常
     * @return 失败响应
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public CommonResponse<Void> handleMethodArgumentNotValidException(
        MethodArgumentNotValidException exception
    ) {
        return CommonResponse.fail("PARAM_ERROR", "请求参数不正确");
    }

    /**
     * 处理业务异常。
     *
     * @param exception 业务异常
     * @return 失败响应
     */
    @ExceptionHandler(BizException.class)
    public CommonResponse<Void> handleBizException(BizException exception) {
        return CommonResponse.fail(exception.getCode(), exception.getMessage());
    }

    /**
     * 处理统一前置校验异常。
     *
     * @param exception 前置校验异常
     * @return 失败响应
     */
    @ExceptionHandler(IllegalArgumentException.class)
    public CommonResponse<Void> handleValidateException(IllegalArgumentException exception) {
        return CommonResponse.fail("PARAM_ERROR", exception.getMessage());
    }

    /**
     * 处理未知异常。
     *
     * @param exception 未知异常
     * @return 失败响应
     */
    @ExceptionHandler(Exception.class)
    public CommonResponse<Void> handleException(Exception exception) {
        return CommonResponse.fail("SYSTEM_ERROR", "系统繁忙，请稍后重试");
    }
}
```

## 18. 测试与交付规范

建议测试分层：

- `T1`：平台、权限、数据范围、审计
- `T2`：业务模块主链路
- `T3`：财务主链路
- `T4`：全链路回归与上线前冒烟

强制规则：

- 每个模块开发完成后，必须对该模块全部 API 做回归测试
- 不能只测本次改动接口
- 提测前必须输出模块级 API 回归清单与结果
- 新增或修改的关键类、方法必须同步检查中文注释是否补齐
- 评审清单中必须包含“命名、注释、边界、异常、空值、事务、锁、幂等、自测结果”项

上线前检查：

- 是否统一 `UTF-8`
- 是否按模块拆分与分层边界实现
- 是否补齐逻辑删除与审计字段
- 是否把复杂 SQL 放入 XML
- 是否把 Request 隔离在 `web` 或 `interfaces` 层
- 是否补齐权限、幂等、分布式锁、审计、`TraceId`
- 是否消除魔法字符串与魔法数字
- 是否补齐关键类、关键方法、关键分支的中文注释

## 19. 团队落地要求

建议团队按以下方式执行：

1. 新项目创建时先放入本文档。
2. 开发前先按项目或需求划分模块，再确认聚合、权限、数据范围、幂等、审计需求。
3. 开发时默认把“中文注释”和“代码质量自检”作为交付标准的一部分。
4. 代码评审时按本文档逐项检查。
5. 每个模块开发完成后，必须对该模块全部 API 完成回归测试。
6. 提测前输出模块级回归清单与结果。
7. 后续新增规则时优先更新本文档，不要散落在聊天记录里。
