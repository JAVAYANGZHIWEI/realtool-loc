"""论文主结果图：8 款模型在 ELV 基线与 Protected-Slot 策略下的 CorePASS 对比。

数据与 README 主结果表一致（论文全量实验，16,384 条答案）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MODELS = ["Qwen3-32B", "DeepSeek\nV4 Flash", "DeepSeek\nV4 Pro", "DeepSeek\nV3.2",
          "Qwen3.6-35B", "GPT-5.1", "Claude Sonnet\n4.6 Thinking", "Kimi K2\nThinking"]
ELV = [44.14, 55.27, 48.44, 38.67, 35.94, 75.98, 66.41, 55.08]
PROT = [59.18, 83.20, 85.55, 74.80, 60.74, 81.05, 85.74, 78.91]
DELTA = [round(p - e, 2) for e, p in zip(ELV, PROT)]

x = range(len(MODELS))
w = 0.38
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
b1 = ax.bar([i - w / 2 for i in x], ELV, w, label="ELV baseline", color="#6b8ec9")
b2 = ax.bar([i + w / 2 for i in x], PROT, w, label="Protected-Slot", color="#e09656")

for i, (e, p, d) in enumerate(zip(ELV, PROT, DELTA)):
    ax.text(i - w / 2, e + 1.2, f"{e:.1f}", ha="center", fontsize=7.5)
    ax.text(i + w / 2, p + 1.2, f"{p:.1f}", ha="center", fontsize=7.5)
    ax.text(i, 93, f"+{d:.1f}", ha="center", fontsize=8, color="#b23a2e", fontweight="bold")

ax.axhline(52.49, ls="--", lw=1, color="#777")
ax.text(7.4, 53.6, "baseline avg 52.49", fontsize=7.5, color="#555", ha="right")
ax.set_xticks(list(x))
ax.set_xticklabels(MODELS, fontsize=8)
ax.set_ylabel("CorePASS (%)", fontsize=10)
ax.set_ylim(0, 100)
ax.yaxis.grid(True, ls=":", lw=0.6, alpha=0.5)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=9, frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("results/figures/corepass_by_model.png")
print("saved results/figures/corepass_by_model.png")