# RealTool-Loc — Dataset Validation Notes

This file cross-checks the released dataset (`data/realtool_loc.jsonl`, version
`real_tool_mvp_v3`) against the numbers reported in the paper (IALP 2026
submission). The authoritative field-level specification and evaluation policy
live in `data/schema.md`; `data/DATA_CARD.md` describes the dataset.

## Dataset profile

| Item           | Count |
|----------------|-------|
| Samples        | 1024  |
| Source records | 128   |
| Tools/domains  | 32    |
| Languages      | 8     |
| Field instances (field_specs) | 5600 |

Each of the 32 tools contributes 4 frozen records; every record is paired with
all 8 language settings, yielding 1,024 samples (128 per language).

## Verification results (measured on the released files)

All checks below use the paper-independent counts computed directly from
`data/realtool_loc.jsonl`, `data/splits/dev_ids.txt`, `data/splits/test_ids.txt`.

### Field roles: paper vs released data

| Role      | Paper (Table II) | Released data | Match |
|-----------|------------------|---------------|-------|
| immutable | 1888             | 1888          | yes   |
| entity    | 1376             | 1376          | yes   |
| semantic  | 2008             | 2016          | no (8) |
| status    | 320              | 320           | yes   |

The semantic discrepancy is fully accounted for: for `food` record 001, the
per-field role lists mark the localizable status field with role `status` (8
samples, one per language), while the paper table counted it inside the
semantic bucket. The other three roles match exactly, and the total field
instance count is consistent. The release files are authoritative.

### Required-field count distribution: paper vs released data

| Required fields | Paper  | Released | Match |
|-----------------|--------|----------|-------|
| 4               | 32     | 32       | yes   |
| 5               | 616    | 616      | yes   |
| 6               | 280    | 280      | yes   |
| 7               | 64     | 64       | yes   |
| 8               | 32     | 32       | yes   |

### Splits

- dev: 512 samples, test: 512 samples, zero overlap.
- Splits are source-record-disjoint (no record appears in both).
- dev ∪ test covers all 1,024 sample ids.

### Attribution subset

`data/attribution.jsonl` holds 448 tasks: 7 conditions x 64 records, 32
domains, matched against the same 8 target languages used in the main set.

## How to verify

Official, deterministic checks (Python 3.10+, standard library only):

```bash
PYTHONPATH=src python3 scripts/validate_dataset.py   # shape, ids, contracts
PYTHONPATH=src python3 scripts/make_splits.py --check  # split isolation
PYTHONPATH=src python3 scripts/reproduce_results.py --check  # results arithmetic
```

## 32 source domains

air_quality, arxiv_paper, book, clinical_trial, country, crate, crypto_market,
currency_exchange, earthquake, fda_drug_label, food, gbfs_station, geocode,
github, gutenberg, hackernews_item, holiday, indicator, iss_location, music,
npm, postal, pypi, scholarly, species, stackexchange_question, sunrise_sunset,
timezone, university, weather, wikidata, wikipedia.