# RealTool-Loc

**评估多语言工具增强型 LLM Agent 忠实性的基准，以及把忠实性提升 +23.66pp 的 Protected-Slot 占位符策略**

论文：*From Tool Results to User Answers: Benchmarking Faithful Multilingual Realization in LLM Agents*（IALP 2026 投稿，第二作者）。本仓库随论文发布完整制品：1024 任务基准数据（`data/`）、确定性评估器（`src/realtool_loc/`）、四套实现策略 prompt（`prompts/`）与全部结果表（`results/`），评估代码零外部依赖，可直接复现论文数字。

[![CI](https://img.shields.io/github/actions/workflow/status/JAVAYANGZHIWEI/realtool-loc/ci.yml?branch=main)](https://github.com/JAVAYANGZHIWEI/realtool-loc/actions)
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Main Results

**图 1：8 款模型在 ELV 基线与 Protected-Slot 策略下的 CorePASS（均值 52.49 → 76.15）**

![corepass-by-model](results/figures/corepass_by_model.png)

`scripts/plot_results.py` 可复现上图，数据与下表同源（8 模型 × 4 策略 × 512 测试任务 = 16,384 条答案）。

从图里可以读出几个现象：

- **8/8 全正**：没有一款模型因为占位符化而受损，增益 +5.07 ~ +37.11pp
- **受益最大的是中低档模型**：DeepSeek V4 Pro（+37.11）、V3.2（+36.13）这类基线更容易改写字段值的模型，保护收益也最大；基线最强的 GPT-5.1 只 +5.07——基线能力越强，占位符能补的洞越小
- **平均线上移 23.66pp**：52.49% → 76.15%，95%CI [18.16, 29.32]
- **增益不是单类任务撑起来的**：96 个"多词英文语义文本"任务 31.77% → 87.11%（贡献 43.86% 新增通过），扣除后其余 416 任务仍 +16.35pp

## Background

Agent 调用工具时，评测通常只看"最终答案像不像"，没人检查填参数时是不是瞎填：航班号不存在也照样填进去（幻觉字段），用户明确给出的不可变信息被悄悄改写。低资源语种（藏语、维语、传统蒙文、阿拉伯字母哈萨克语等）连评测数据都是空白——忠实性无法量化，就无法横向对比模型，也无从定位错误环节。

## Dataset

基准数据随仓库发布（`data/`，版本 `real_tool_mvp_v3`），静态、无实时 API 依赖：

- **构成**：32 个公开工具/服务 × 每工具 4 条静态记录 × 8 语种 = **1,024 任务**（dev/test 各 512，源记录不相交）
- **语种**：中文、日语、泰语、印尼语、藏语、维语、传统蒙古文（mn-Mong）、阿拉伯字母哈萨克语（kk-Arab）；低资源语种用于暴露脚本控制与本地化失败
- **字段角色**：4 类——不可变（标识符，1888 实例）、实体（1376）、语义（2016）、状态（仅状态字段要求显式本地化，320）；每样本必需字段 4~8 个，分布 32/616/280/64/32
- **attribution 子集**：448 任务（7 条件 × 64 记录），用于对照诊断忠实性归因
- 文件清单、schema 与论文一致性核对见 `data/README.md`

每个任务含：目标语种用户查询、冻结的工具返回记录、逐字段角色标注（field_specs）、必需字段清单、可接受等价变体、预定义的不支持断言（幻觉检查用）。

## Method

**Protected-Slot** 分两阶段：把不可变/实体/语义类字段值替换成 `[[FIELD_xxx]]` 占位符后再让模型生成，生成完确定性还原；需要本地化的状态字段保持模型生成。动机是防乱编，不是防失败——缺失字段被占位符保护时显式声明缺失、其他字段照常执行，而不是靠模型猜。

本次发布四套实现策略（`prompts/`）：

| 策略 | 说明 |
|---|---|
| `naive` | 直接给共享载荷，无显式字段策略指令 |
| `field_constrained` | 显式暴露必需字段与字段角色 |
| `extract_localize_verify`（ELV） | 单次调用内：提取证据 → 本地化实现 → 自检覆盖 |
| `protected_slot_realization` | 生成期把可保护字段替换为确定性占位符，事后还原 |

仓库只负责渲染消息，不绑定任何模型厂商；两段式消息可发给任意兼容的对话接口，把最终答案按下方格式保存后评测。

## Evaluation

**CorePASS 复合指标** = 7 项确定性检查连乘——语言/脚本控制 L · 必需字段覆盖 C · 不可变保持 I · 实体保真 E · 语义保真 S · 本地化 Z · 无幻觉 H。一项不过整体 FAIL，无法用强项补偿；规则化、零成本、可复现。

预测输入为 JSON Lines（三字段，`id` 必须匹配发布任务，未知 id 直接拒绝）：

```json
{"id": "weather_zh_001", "method": "my_method", "answer": "..."}
```

- `strict`：论文的精确复写契约（默认，主表数字来源）
- `relaxed`：额外接受文档化的自然语言等价表达（国家、货币、语言代码等元数据字段）

消融：4 模型 × 64 记录 × 7 条件复合对比诊断（英-多语言差异最大 30.9–37.1pp；显式证据契约 +12.9/+8.2pp）。

双辅助评估：Gemini 3.1 Pro 抽 30% 样本评语义忠实（44.64→64.20）；Claude Sonnet 4.6 Thinking 独立抽 30% 评自然度（3.838→3.475，Δ−0.363 诚实披露）——主指标不依赖 LLM 裁判。

## Results

| 模型 | ELV (%) | Protected (%) | Δ (pp) |
|---|---|---|---|
| Qwen3-32B-4bit | 44.14 | 59.18 | +15.04 |
| DeepSeek V4 Flash | 55.27 | 83.20 | +27.93 |
| DeepSeek V4 Pro | 48.44 | 85.55 | **+37.11** |
| DeepSeek V3.2 | 38.67 | 74.80 | +36.13 |
| Qwen3.6-35B-A3B (无思考) | 35.94 | 60.74 | +24.80 |
| GPT-5.1 | **75.98** | 81.05 | +5.07 |
| Claude Sonnet 4.6 Thinking | 66.41 | **85.74** | +19.33 |
| Kimi K2 Thinking | 55.08 | 78.91 | +23.83 |
| **平均** | **52.49** | **76.15** | **+23.66** |

全部按语言、模型、策略细分的 frozen 结果表在 `results/`（`main_table.csv`、`language_results.csv`、`significance.csv` 等）。

## Reproduction

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest          # 全部测试（官方回归 + 复刻层）
PYTHONPATH=src python3 scripts/validate_dataset.py       # 数据集完整校验
PYTHONPATH=src python3 scripts/make_splits.py --check    # 拆分不变量
PYTHONPATH=src python3 scripts/reproduce_results.py --check  # 复现论文结果数字
PYTHONPATH=src python3 scripts/evaluate_predictions.py \
  --predictions examples/predictions.jsonl --output /tmp/example.strict.json \
  --evaluation-policy strict
PYTHONPATH=src python3 scripts/render_prompt.py --sample-id weather_zh_001 \
  --method protected_slot_realization
python -m src.corepass_checker   # 复刻层演示（4 case）
```

复刻层真实输出（4 个 case 覆盖三类核心判定）：

```
PASS | 查询公司名:统信软件 金额:5200 | -                     <- 全字段正确
PASS | 查询公司名:统信软件 金额:5200 | -                     <- 缺公司名但 Protected-Slot 保护
FAIL | 查询公司名:统信软件 金额:5200 | 不可变字段被改写: 公司名  <- 不可变信息被篡改
FAIL | 查询公司名:统信软件 金额:5200 | 类型失配: 金额(期望int, 得到str)
CorePASS: 2/4 通过  (论文: Protected-Slot策略 76.15% vs 基线52.49%, +23.66pp)
```

`reproduce_results.py --check` 从 `results/main_table.csv` 重算 headline 数值并与 `results/reported_aggregates.json` 比对，不需要再花模型调用；本仓库不声称对专有模型生成或外部 LLM 评判做逐位复现，可审计的离线部分是：数据契约、prompts、确定性评估器、frozen 结果表、smoke 预测。

## Data Notes

实测与论文的一致性核对见 `data/SCHEMA.md`：除 food 域一条记录的 status/semantic 归类口径差（8 样本）外全部吻合（1024 样本、128 记录、32 域、8 语种、必需字段分布、splits 全部一致）。`retrieved_at` 等 `tool_source` 里的字段是数据集构建元数据，不是每条记录的抓取时间戳。

## License

- 代码：MIT © 2026 JAVAYANGZHIWEI（`LICENSE`）
- 数据：CC BY（`data/LICENSE`）
- 第三方声明：`THIRD_PARTY_NOTICES.md`；上游公开工具/API 材料仍受其各自提供方条款约束