# Java 后端编码规范

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

- AI 生成或修改代码时，中文注释属于强制要求，不需要等待用户单独提出
- 注释默认语言统一为中文，禁止在同一套后端规范代码中随意混用英文注释
- 注释必须服务于“可维护性”和“业务可读性”，不要写成噪音
- 对关键业务字段，必须补齐字段级中文注释，且注释语义要清晰到足以支撑维护、联调和评审
- 类、`public` / `protected` 方法、Repo 方法、关键业务字段、关键分支的中文注释都属于强制检查项

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

类可以按需要使用注解，例如 `@Builder`、`@Getter`、`@Data`、`@NoArgsConstructor`、`@AllArgsConstructor`、`@Slf4j`、`@Service`、`@Component`、`@Configuration` 等，但注解不能替代类注释本身，也不能替代关键字段和关键方法的语义说明。

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

以下字段必须补充中文注释：

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

简单 DTO / VO / Request / Response 中名称非常直观、且没有额外业务语义的字段，可以在类注释已说明上下文时不重复逐字段展开；但只要字段承担状态、金额、权限、风控、外部映射、兼容分支等关键语义，就必须写清楚。

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

- `@Data`、`@Getter`、`@Builder` 等注解可以正常使用
- 注解用于减少样板代码，不承担业务语义表达职责
- 只要字段本身承载关键业务语义，仍然要写清晰的字段注释

#### 8.4.3 纯数据载体对象的注解约束

`Request`、`Response`、`Command`、`Query`、`VO` 这类纯数据载体对象，默认遵循以下规则：

- 同时需要 getter / setter 的可变数据载体，默认优先使用 `@Data`
- 只需要只读访问的对象，优先使用 `@Getter`
- 需要链式构建、参数较多、存在可选字段时，再按需增加 `@Builder`
- 枚举默认使用 `@Getter` 即可，不要给枚举加 `@Setter`
- 不要为纯字段读写手写 getter / setter
- 只有在框架兼容要求、序列化约束、访问控制定制、字段派生逻辑等场景下，才允许手写访问方法
- 即使用了注解，类注释和关键字段中文注释仍然不能省略

推荐写法示例：

```java
/**
 * 后台确认订单请求参数。
 */
@Data
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

不推荐写法示例：

```java
public class ConfirmOrderRequest {

    @NotBlank(message = "订单号不能为空")
    private String orderNo;

    @Size(max = 200, message = "备注长度不能超过 200")
    private String remark;

    public String getOrderNo() {
        return orderNo;
    }

    public void setOrderNo(String orderNo) {
        this.orderNo = orderNo;
    }

    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark;
    }
}
```

补充示例：

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
    CONFIRMED(2, "已确认");

    private final Integer code;
    private final String description;
}
```

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