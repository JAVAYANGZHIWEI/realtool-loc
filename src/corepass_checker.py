"""CorePASS 判定逻辑的最小实现：字段缺失 / Protected-Slot 占位符 / 类型匹配。
用法: python -m src.corepass_checker
"""
from __future__ import annotations
import sys
from dataclasses import dataclass, field


@dataclass
class Slot:
    name: str            # 字段名
    role: str            # 字段角色: immutable(不可变)/entity(实体)/semantic(语义)/state(状态)
    expected_type: str   # str/int/bool
    is_protected: bool = False  # 是否Protected-Slot（缺失时填[Protected]占位符而非拒绝）

@dataclass
class Case:
    task: str
    slots: list[Slot]
    answer: dict         # 模型返回的字段dict


def check(case: Case) -> tuple[bool, list[str]]:
    """返回 (是否通过CorePASS, 失败原因列表)"""
    failures: list[str] = []
    for s in case.slots:
        if s.name not in case.answer:
            if s.is_protected:
                continue  # 占位符保护：缺失不算硬失败（论文机制核心）
            failures.append(f"缺失字段: {s.name}")
            continue
        v = case.answer[s.name]
        # 类型检查（简化版：int/bool 单独处理）
        if s.expected_type == "int" and not isinstance(v, int):
            failures.append(f"类型失配: {s.name}(期望int, 得到{type(v).__name__})")
        if s.expected_type == "bool" and not isinstance(v, bool):
            failures.append(f"类型失配: {s.name}(期望bool, 得到{type(v).__name__})")
        # 不可变字段必须逐字一致（这里用task内关键词粗验，完整版是双语对齐）
        if s.role == "immutable" and s.name in task_to_value(case.task) and v != task_to_value(case.task)[s.name]:
            failures.append(f"不可变字段被改写: {s.name}")
    return (len(failures) == 0, failures)


def task_to_value(task: str) -> dict:
    """模拟从任务文本解析出的期望值（真实版是字段角色分类器+双语对齐）"""
    pairs = {}
    for kw in ("公司名", "金额"):
        if kw in task:
            import re
            m = re.search(kw + r"[:：](\S+)", task)
            if m:
                pairs["公司名" if kw == "公司名" else "金额"] = m.group(1)
    return pairs


def main() -> None:
    cases = [
        Case("查询公司名:统信软件 金额:5200", [Slot("公司名","immutable","str",True), Slot("金额","entity","int")], {"公司名":"统信软件","金额":5200}),
        Case("查询公司名:统信软件 金额:5200", [Slot("公司名","immutable","str",True), Slot("金额","entity","int")], {"金额":5200}),          # 缺公司名但被保护
        Case("查询公司名:统信软件 金额:5200", [Slot("公司名","immutable","str",True), Slot("金额","entity","int")], {"公司名":"其他公司","金额":5200}),  # 不可变被改写
        Case("查询公司名:统信软件 金额:5200", [Slot("公司名","immutable","str",True), Slot("金额","entity","int")], {"公司名":"统信软件","金额":"5200"}),  # 类型失配
    ]
    passed = 0
    for c in cases:
        ok, fails = check(c)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} | {c.task[:24]:<26} | {('; '.join(fails) or '-')[:40]}")
    print(f"\nCorePASS: {passed}/{len(cases)} 通过"
          f"  (论文: Protected-Slot策略 76.15% vs 基线52.49%, +23.66pp)")


if __name__ == "__main__":
    main()
