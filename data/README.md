# Data

Frozen benchmark dataset for RealTool-Loc: faithful multilingual realization of
tool results (1,024 tasks, 128 source records, 32 public tools, 8 language
settings, dataset version `real_tool_mvp_v3`).

| File | Description |
|------|-------------|
| `realtool_loc.jsonl` | 1,024 main tasks (one JSON object per line) |
| `attribution.jsonl` | 448 controlled-attribution tasks (7 conditions x 64 records) |
| `attribution.manifest.json` | Manifest for the attribution subset |
| `tool_sources.json` | 32 public tool/API source contexts (provider, docs, request URLs) |
| `schema.md` | Authoritative field-level schema and evaluation policy |
| `SCHEMA.md` | Paper cross-check and validation notes (measured counts) |
| `DATA_CARD.md` | Dataset card |
| `splits/dev_ids.txt` | 512 dev sample ids (record-disjoint) |
| `splits/test_ids.txt` | 512 test sample ids (record-disjoint) |
| `LICENSE` | Dataset license (CC BY; see `../LICENSE` for the code) |

## Provenance

The dataset is the frozen benchmark behind the paper. It ships inside this
repository in full: every sample carries the source record, per-field role
annotations, accepted evaluation variants, and predefined unsupported claims,
so the deterministic evaluator runs fully offline with no live API dependency.

## Integrity

Verified with the official checker:

```bash
PYTHONPATH=src python3 scripts/validate_dataset.py
```

The release data matches the paper on all counts except one documented
classification nuance: for `food` record 001 (8 samples), the localizable
status field carries role `status` in the field specs, where the paper table
counted it as semantic. Details in `SCHEMA.md`. Splits are static and
record-disjoint; any future revision increments the dataset version instead of
mutating these files.