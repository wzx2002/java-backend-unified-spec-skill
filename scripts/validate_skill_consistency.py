#!/usr/bin/env python3
"""Validate internal consistency for the java-backend-unified-spec skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "java-backend-unified-spec"

SKILL_FILE = SKILL_DIR / "SKILL.md"
ARCH_FILE = SKILL_DIR / "references" / "architecture-and-boundaries.md"
CODING_FILE = SKILL_DIR / "references" / "coding-standards.md"
CODE_FILE = SKILL_DIR / "references" / "code-examples.md"
CHECKLIST_FILE = SKILL_DIR / "references" / "templates-and-checklists.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_relative_markdown_links(path: Path, errors: list[str]) -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    text = _read_text(path)
    for target in pattern.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        relative_target = target.split("#", 1)[0]
        if not relative_target:
            continue
        resolved_path = (path.parent / relative_target).resolve()
        if not resolved_path.exists():
            errors.append(f"{path.name}: missing linked file -> {target}")


def _require_snippets(path: Path, snippets: list[str], errors: list[str]) -> None:
    text = _read_text(path)
    for snippet in snippets:
        if snippet not in text:
            errors.append(f"{path.name}: missing required snippet -> {snippet}")


def _forbid_snippets(path: Path, snippets: list[str], errors: list[str]) -> None:
    text = _read_text(path)
    for snippet in snippets:
        if snippet in text:
            errors.append(f"{path.name}: forbidden legacy snippet still present -> {snippet}")


def _forbid_regex(path: Path, patterns: list[str], errors: list[str]) -> None:
    text = _read_text(path)
    for pattern in patterns:
        if re.search(pattern, text, re.MULTILINE | re.DOTALL):
            errors.append(f"{path.name}: forbidden legacy pattern still present -> {pattern}")


def _require_regex(path: Path, patterns: list[str], errors: list[str]) -> None:
    text = _read_text(path)
    for pattern in patterns:
        if not re.search(pattern, text, re.MULTILINE | re.DOTALL):
            errors.append(f"{path.name}: missing required pattern -> {pattern}")


def main() -> int:
    errors: list[str] = []

    markdown_files = sorted(SKILL_DIR.rglob("*.md"))
    for path in markdown_files:
        _check_relative_markdown_links(path, errors)

    _require_snippets(
        SKILL_FILE,
        [
            "For failures that must expose stable business error codes, such as not-found, update-failed, or status-illegal semantics, use `BizException` or a project-level business assert/helper instead of naked `Validate`.",
            "Repo write methods should usually return `boolean`, affected-row count, saved entity identity, or typed result;",
            "`ObjectUtil.equal(...)` / `notEqual(...)` for null-safe equality",
            "`BooleanUtil.isTrue(...)` / `isFalse(...)` for boxed or tri-state boolean flags",
        ],
        errors,
    )
    _forbid_snippets(
        SKILL_FILE,
        [
            "do not let Repo or RepoImpl throw business exceptions for update-failed, not-found, or status-illegal semantics.",
        ],
        errors,
    )

    _require_snippets(
        ARCH_FILE,
        [
            "单对象 Repo 查询默认允许返回 `null` 表示查无数据；如项目已经统一使用 `Optional`，在同一模块内保持一致即可",
            "复杂条件写操作如调用方需要区分失败原因，可返回显式结果对象、枚举或其他 typed result",
        ],
        errors,
    )

    _require_snippets(
        CODING_FILE,
        [
            "对需要稳定业务错误码的失败语义，不要直接使用裸 `Validate`，应使用 `BizException` 或项目统一业务异常断言能力翻译",
            "单对象 Repo 查询默认允许返回 `null`，由 `ServiceImpl`、`domain` 或统一业务断言能力翻译成业务语义",
            "复杂条件写操作如调用方需要区分失败原因，可返回显式结果对象、枚举或其他 typed result",
            "对象相等判断强制使用 `ObjectUtil.equal(...)`、`ObjectUtil.notEqual(...)`",
            "默认使用 `BooleanUtil.isTrue(...)`、`BooleanUtil.isFalse(...)`",
        ],
        errors,
    )
    _forbid_snippets(
        CODING_FILE,
        [
            "由 `ServiceImpl` 负责使用 `Validate.isTrue(...)`、`Validate.notNull(...)` 或统一业务异常机制收口",
            "Validate.notNull(employeeDO, AccountErrorMessages.EMPLOYEE_NOT_FOUND);",
            "Validate.isTrue(updated, AccountErrorMessages.EMPLOYEE_UPDATE_FAILED);",
        ],
        errors,
    )

    _require_snippets(
        CHECKLIST_FILE,
        [
            "是否错误地用裸 `Validate` 承担需要稳定业务错误码的失败语义",
            "复杂条件写操作是否被不加区分地压成 `boolean`",
            "`Objects.equals(...)`",
            "`Boolean.TRUE.equals(...)`",
        ],
        errors,
    )

    _require_snippets(
        CODE_FILE,
        [
            "BizAssert.notNull(orderDO, OrderErrorCodes.ORDER_NOT_FOUND, OrderErrorMessages.ORDER_NOT_FOUND);",
            "BizAssert.isTrue(updated, OrderErrorCodes.ORDER_CONFIRM_FAILED, OrderErrorMessages.ORDER_CONFIRM_FAILED);",
            "public static final String ORDER_CONFIRM_FAILED = \"ORDER_CONFIRM_FAILED\";",
            "public static final String ORDER_CONFIRM_FAILED = \"订单确认失败\";",
            "return ObjectUtil.equal(PENDING.getCode(), code);",
        ],
        errors,
    )
    _require_regex(
        CODE_FILE,
        [
            r"BizAssert\.isTrue\(\s*OrderStatusEnum\.isPending\(orderDO\.getStatus\(\)\),\s*OrderErrorCodes\.ORDER_STATUS_INVALID,\s*OrderErrorMessages\.ORDER_STATUS_INVALID\s*\);",
        ],
        errors,
    )
    _forbid_snippets(
        CODE_FILE,
        [
            "@ExceptionHandler(NullPointerException.class)",
            "throw new BizException(OrderErrorCodes.ORDER_NOT_FOUND, OrderErrorMessages.ORDER_NOT_FOUND);",
            "throw new BizException(OrderErrorCodes.ORDER_STATUS_INVALID, OrderErrorMessages.ORDER_STATUS_INVALID);",
            "throw new BizException(OrderErrorCodes.ORDER_CONFIRM_FAILED, OrderErrorMessages.ORDER_CONFIRM_FAILED);",
            "Validate.notNull(orderDO, OrderErrorMessages.ORDER_NOT_FOUND);",
            "Validate.isTrue(updated, OrderErrorMessages.ORDER_CONFIRM_FAILED);",
        ],
        errors,
    )
    _forbid_regex(
        CODE_FILE,
        [
            r"Validate\.isTrue\(\s*OrderStatusEnum\.isPending\(orderDO\.getStatus\(\)\),\s*OrderErrorMessages\.ORDER_STATUS_INVALID",
        ],
        errors,
    )

    if errors:
        print("java-backend-unified-spec consistency check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("java-backend-unified-spec consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
