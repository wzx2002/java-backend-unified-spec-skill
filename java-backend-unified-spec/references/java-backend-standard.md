# Java 后端统一开发规范与示例模板

## 1. 目标

本文档用于作为后续所有 Java 后端项目的统一规范基线。

适用场景：

- 新建 Java 后端项目
- 老项目重构
- 团队统一编码口径
- AI 协作开发
- 代码评审、提测、交付验收

本文档是独立规范，不依赖当前仓库其他文档。

---

## 2. 建议技术基线

推荐默认技术栈：

- `Java 25`
- `Spring Boot 3`
- `Maven`
- `MyBatis-Plus`
- `MyBatis XML`
- `Redis`
- `JWT access token + refresh token`
- `Lombok`
- `jakarta validation`
- 全项目统一 `UTF-8`
- 数据库统一 `utf8mb4`

统一要求：

- 源码、配置、SQL、XML、YAML、Properties、Markdown、脚本统一使用 `UTF-8`
- 禁止提交 `GBK`、`ANSI`、`BOM` 文件
- 单表简单查询与状态更新优先使用 `MyBatis-Plus Wrapper`
- 多表联查、统计、导出、对账统一使用 `Mapper XML`

---

## 3. 建议安装的 Skills

基础必备：

- `bangyi-project`
- `bangyi-java-ddd`

按场景追加：

- `bangyi-permission-datascope`
- `bangyi-finance-audit`
- `bangyi-test-delivery`
- `bangyi-frontend-antd`

最小组合建议：

- 普通 Java 后端项目：`bangyi-project` + `bangyi-java-ddd`
- 带权限与数据隔离：再加 `bangyi-permission-datascope`
- 带资金链路：再加 `bangyi-finance-audit`
- 进入提测与上线阶段：再加 `bangyi-test-delivery`

---

## 4. 顶层模块命名与工程结构

新项目顶层模块命名统一优先使用：

- `project-infrastructure`
- `project-persistence`
- `project-business`
- `project-web`
- `project-integration`，可选，仅当第三方接入很多时拆分

补充规则：

- 如果项目同时存在 HTTP、MQ、定时任务、Webhook 等多入口，`project-web` 升级为 `project-interfaces`
- `integration` 属于基础设施边界，不是业务层
- 不推荐新项目继续使用 `framework / model / service / application` 作为顶层模块名
- `business` 是顶层业务模块名，模块内部依然可以保留 `service / service/impl` 目录
- `persistence` 是顶层数据访问模块名，模块内部实体目录依然统一使用 `model`

标准结构：

```text
project-parent
├─ project-infrastructure
├─ project-persistence
├─ project-business
├─ project-web
└─ project-integration (optional)
```

多入口项目结构：

```text
project-parent
├─ project-infrastructure
├─ project-persistence
├─ project-business
├─ project-interfaces
└─ project-integration (optional)
```

旧命名映射关系：

- `framework` -> `infrastructure`
- `model` -> `persistence`
- `service` -> `business`
- `application` -> `web`

---

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

---

## 6. 分层职责与边界

### 6.1 infrastructure 层职责

负责基础设施能力：

- 基础配置
- MyBatis-Plus
- 逻辑删除全局配置
- 分页
- 防抖
- 幂等
- Redis 分布式锁
- 权限与数据范围基础能力
- 审计日志
- 登录日志与操作日志
- 风控
- TraceId
- JWT
- Redis
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

- 单表简单查询使用 `Wrappers.lambdaQuery(...)`
- 单表状态更新使用 `Wrappers.lambdaUpdate(...)`
- 多表联查、统计、导出、对账统一进入 `Mapper.xml`
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

---

## 7. 命名规范

### 7.1 目录命名

- 实体目录统一使用 `model`
- 禁止使用 `do` 作为目录名
- 枚举统一放 `enums`
- XML 统一放 `resources/mapper/**`

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

禁止出现魔法字符串和魔法数字。

常量类统一按类别命名，不要把所有内容塞进 `Constants`：

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

---

## 8. 数据库规范

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

---

## 9. 安全、权限与风控规范

### 9.1 JWT 鉴权

- `/api/**` 只接受前台 Token
- `/admin/**` 只接受后台 Token
- 前后台必须使用两套 `SecurityFilterChain`
- 匿名放行接口仅限 `login / register / send-sms / refresh-token`
- `logout`、`me`、资料修改、业务查询等接口必须要求有效 Access Token
- 前后台 Token 必须区分 `tokenType`、`issuer`、`audience`
- 前后台缓存、黑名单、Refresh Token 命名空间必须隔离

### 9.2 长期登录

- 不允许超长 Access Token 直接长期登录
- 必须采用 `短效 access token + 长效 refresh token`
- Refresh Token 必须可控、可吊销、可失效、可审计
- Logout 时至少吊销当前操作人的 Refresh Token

### 9.3 五层权限模型

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

### 9.4 防抖、幂等、并发控制

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

- 并发控制默认统一使用 Redis 分布式锁
- 默认禁止乐观锁、`version` 字段竞争更新、数据库行版本控制方案
- 锁组件统一放 `infrastructure`
- 锁使用位置统一在 `business` 或 `domain manager`
- 优先提供闭包式执行接口，如 `executeWithLock(...)`
- 锁获取失败时统一抛业务异常，不允许静默吞掉
- 锁 Key 必须稳定、可预测、可审计

### 9.5 日志与审计

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

---

## 10. 异常与响应规范

统一原则：

- 所有接口异常统一由 `GlobalExceptionHandler` 收口
- 不允许每个 Controller 单独写大段 `try/catch`
- 异常分类必须明确
- 前后台统一使用同一套响应结构

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

---

## 11. 第三方接入规范

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

---

## 12. 财务项目附加规则

只要项目涉及资金链路，额外强制：

- 金额真实来源只认事实表
- 已确认记录禁止直接改金额，只能冲销
- 确认、冲销、付款、发放接口必须幂等
- 有天然业务单号的动作直接以业务单号做幂等键
- 无天然业务单号的动作必须显式传 `requestNo`
- 资金流水必须与确认动作同事务落库
- 审计日志必须记录前值、后值、原因、`TraceId`
- 对账必须能校验事实表与资金流水一致

---

## 13. 类模板清单

### 13.1 infrastructure 层最少应具备

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

### 13.2 persistence 层最少应具备

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

### 13.3 business 层最少应具备

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

### 13.4 web / interfaces 层最少应具备

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

### 13.5 integration 层最少应具备

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

---

## 14. 单流程标准写法

以“后台确认完单”为例，标准链路如下：

1. `web` 接收请求并完成参数校验。
2. `web` 通过 Assembler 转成 `business` Command。
3. `business` 统一处理权限、防抖、日志、事务。
4. `business` 在业务主键维度执行 Redis 分布式锁。
5. `business` 调用 `persistence` 查询数据。
6. `domain` 校验状态并处理状态流转。
7. `persistence` 使用 Wrapper 落库。
8. AOP 或事件统一记录日志、审计和风控信息。

---

## 15. 代码示例

### 15.1 基础实体示例

```java
/**
 * 业务基础实体
 */
public class BaseDO {

    /**
     * 创建时间
     */
    private LocalDateTime createdAt;

    /**
     * 更新时间
     */
    private LocalDateTime updatedAt;

    /**
     * 创建人
     */
    private Long createdBy;

    /**
     * 更新人
     */
    private Long updatedBy;

    /**
     * 逻辑删除标记
     */
    private Integer isDeleted;

    /**
     * 删除时间
     */
    private LocalDateTime deletedAt;
}
```

### 15.2 常量与枚举示例

```java
public final class OrderErrorCodes {

    public static final String ORDER_NOT_FOUND = "ORDER_NOT_FOUND";
    public static final String ORDER_STATUS_INVALID = "ORDER_STATUS_INVALID";

    private OrderErrorCodes() {
    }
}
```

```java
public final class OrderPermissionCodes {

    public static final String ADMIN_ORDER_CONFIRM = "admin-order-confirm";

    private OrderPermissionCodes() {
    }
}
```

```java
public final class OrderRiskRuleCodes {

    public static final String ORDER_CONFIRM_AUDIT = "ORDER_CONFIRM_AUDIT";

    private OrderRiskRuleCodes() {
    }
}
```

```java
public final class OrderNoRepeatKeys {

    public static final String ADMIN_ORDER_CONFIRM = "admin:order:confirm";

    private OrderNoRepeatKeys() {
    }
}
```

```java
public final class OrderLockKeys {

    public static final String CONFIRM_ORDER_PREFIX = "order:confirm:";

    private OrderLockKeys() {
    }

    public static String confirmOrder(String orderNo) {
        return CONFIRM_ORDER_PREFIX + orderNo;
    }
}
```

```java
public final class OrderApiPaths {

    public static final String ADMIN_BASE = "/admin/order";
    public static final String CONFIRM_ORDER = "/confirm-order";

    private OrderApiPaths() {
    }
}
```

```java
@Getter
@RequiredArgsConstructor
public enum OrderStatusEnum {

    PENDING(1, "待处理"),
    CONFIRMED(2, "已确认"),
    REJECTED(3, "已拒绝");

    private final Integer code;
    private final String description;
}
```

### 15.3 Controller / Request / Assembler 示例

```java
@RestController
@Validated
@RequiredArgsConstructor
@RequestMapping(OrderApiPaths.ADMIN_BASE)
public class AdminOrderController {

    private final OrderService orderService;
    private final AdminOrderWebAssembler adminOrderWebAssembler;

    @PostMapping(OrderApiPaths.CONFIRM_ORDER)
    public CommonResponse<Void> confirmOrder(@Valid @RequestBody ConfirmOrderRequest request) {
        ConfirmOrderCommand command = adminOrderWebAssembler.toConfirmOrderCommand(request);
        orderService.confirmOrder(command);
        return CommonResponse.success();
    }
}
```

```java
public class ConfirmOrderRequest {

    @NotBlank(message = "订单号不能为空")
    private String orderNo;

    @Size(max = 200, message = "备注长度不能超过 200")
    private String remark;
}
```

```java
@Component
public class AdminOrderWebAssembler {

    public ConfirmOrderCommand toConfirmOrderCommand(ConfirmOrderRequest request) {
        return ConfirmOrderCommand.builder()
                .orderNo(request.getOrderNo())
                .remark(request.getRemark())
                .build();
    }
}
```

### 15.4 Command / Service / Domain 示例

```java
@Getter
@Builder
public class ConfirmOrderCommand {

    private final String orderNo;
    private final String remark;
}
```

```java
public interface OrderService {

    void confirmOrder(ConfirmOrderCommand command);
}
```

```java
@Component
public class OrderManager {

    public void validateCanConfirm(OrderDO orderDO) {
        if (!OrderStatusEnum.PENDING.getCode().equals(orderDO.getStatus())) {
            throw new BizException(OrderErrorCodes.ORDER_STATUS_INVALID, "订单状态不允许确认");
        }
    }
}
```

### 15.5 ServiceImpl 示例

```java
@Service
@RequiredArgsConstructor
public class OrderServiceImpl implements OrderService {

    private final OrderRepo orderRepo;
    private final OrderManager orderManager;
    private final DistributedLockExecutor distributedLockExecutor;

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
                    OrderDO orderDO = orderRepo.findByOrderNo(command.getOrderNo());
                    if (orderDO == null) {
                        throw new BizException(OrderErrorCodes.ORDER_NOT_FOUND, "订单不存在");
                    }

                    orderManager.validateCanConfirm(orderDO);
                    orderRepo.confirmOrder(orderDO.getId(), command.getRemark(), OrderStatusEnum.CONFIRMED.getCode());
                });
    }
}
```

### 15.6 Repo / RepoImpl / XML 示例

```java
public interface OrderRepo {

    OrderDO findByOrderNo(String orderNo);

    void confirmOrder(Long id, String remark, Integer status);
}
```

```java
@Repository
@RequiredArgsConstructor
public class OrderRepoImpl implements OrderRepo {

    private final OrderMapper orderMapper;

    @Override
    public OrderDO findByOrderNo(String orderNo) {
        return orderMapper.selectOne(
                Wrappers.lambdaQuery(OrderDO.class)
                        .eq(OrderDO::getOrderNo, orderNo));
    }

    @Override
    public void confirmOrder(Long id, String remark, Integer status) {
        orderMapper.update(
                null,
                Wrappers.lambdaUpdate(OrderDO.class)
                        .eq(OrderDO::getId, id)
                        .set(OrderDO::getStatus, status)
                        .set(OrderDO::getConfirmRemark, remark));
    }
}
```

```xml
<select id="selectOrderPage" resultType="com.example.persistence.order.dto.OrderQueryDTO">
    SELECT
        o.id,
        o.order_no,
        o.status,
        u.nickname AS user_name
    FROM biz_order o
    LEFT JOIN biz_user u ON u.id = o.user_id
    <where>
        <if test="status != null">
            o.status = #{status}
        </if>
    </where>
    ORDER BY o.id DESC
</select>
```

### 15.7 第三方 Client 示例

```java
public interface AiClient {

    String chat(String prompt);
}
```

```java
@Component
@RequiredArgsConstructor
public class XxxAiClient implements AiClient {

    private final AiProperties aiProperties;

    @Override
    public String chat(String prompt) {
        // 这里只做厂商请求封装，不写业务规则
        return "mock-response";
    }
}
```

### 15.8 全局异常处理示例

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public CommonResponse<Void> handleMethodArgumentNotValidException(MethodArgumentNotValidException exception) {
        return CommonResponse.fail("PARAM_ERROR", "请求参数不正确");
    }

    @ExceptionHandler(BizException.class)
    public CommonResponse<Void> handleBizException(BizException exception) {
        return CommonResponse.fail(exception.getCode(), exception.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public CommonResponse<Void> handleException(Exception exception) {
        return CommonResponse.fail("SYSTEM_ERROR", "系统繁忙，请稍后重试");
    }
}
```

---

## 16. 测试与交付规范

建议测试分层：

- `T1`：平台、权限、数据范围、审计
- `T2`：业务模块主链路
- `T3`：财务主链路
- `T4`：全链路回归与上线前冒烟

强制规则：

- 每个模块开发完成后，必须对该模块全部 API 做回归测试
- 不能只测本次改动接口
- 提测前必须输出模块级 API 回归清单与结果

上线前检查：

- 是否统一 `UTF-8`
- 是否按模块拆分与分层边界实现
- 是否补齐逻辑删除与审计字段
- 是否把复杂 SQL 放入 XML
- 是否把 Request 隔离在 `web` 或 `interfaces` 层
- 是否补齐权限、幂等、分布式锁、审计、`TraceId`
- 是否消除魔法字符串与魔法数字

---

## 17. 团队落地要求

建议团队按以下方式执行：

1. 新项目创建时先放入本文档。
2. 开发前先按项目或需求划分模块，再确认聚合、权限、数据范围、幂等、审计需求。
3. 代码评审时按本文档逐项检查。
4. 每个模块开发完成后，必须对该模块全部 API 完成回归测试。
5. 提测前输出模块级回归清单与结果。
6. 后续新增规则时优先更新本文档，不要散落在聊天记录里。
