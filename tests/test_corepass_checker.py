"""CorePASS 核心判定逻辑单元测试——对应论文机制（Protected-Slot / 不可变保持 / 类型匹配）。"""
from src.corepass_checker import Slot, Case, check


def _base_slots():
    return [Slot("公司名", "immutable", "str", True), Slot("金额", "entity", "int")]


def test_all_ok():
    c = Case("查询公司名:统信软件 金额:5200", _base_slots(),
             {"公司名": "统信软件", "金额": 5200})
    ok, fails = check(c)
    assert ok and fails == []


def test_missing_protected_ok():
    # Protected-Slot：缺失字段不判 FAIL（论文核心：显式占位而非拒绝/弃权）
    c = Case("查询公司名:统信软件 金额:5200", _base_slots(), {"金额": 5200})
    ok, _ = check(c)
    assert ok


def test_missing_unprotected_fail():
    c = Case("查询公司名:统信软件 金额:5200",
             [Slot("公司名", "immutable", "str", False), Slot("金额", "entity", "int")],
             {"金额": 5200})
    ok, fails = check(c)
    assert not ok and any("缺失" in f for f in fails)


def test_immutable_rewrite_fail():
    # 不可变字段被篡改 -> FAIL（忠实性约束：不可变信息必须逐字返回）
    c = Case("查询公司名:统信软件 金额:5200", _base_slots(),
             {"公司名": "其他公司", "金额": 5200})
    ok, fails = check(c)
    assert not ok and any("改写" in f for f in fails)


def test_type_mismatch_fail():
    c = Case("查询公司名:统信软件 金额:5200", _base_slots(),
             {"公司名": "统信软件", "金额": "5200"})
    ok, fails = check(c)
    assert not ok and any("类型失配" in f for f in fails)