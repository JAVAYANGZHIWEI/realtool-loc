# RealTool-Loc Benchmark — Dataset Schema

Frozen specification of the RealTool-Loc benchmark dataset (IALP2026 submission).
This file is the machine-readable counterpart of the data card in the paper's
Supplementary Material (Table I/II). Values below are locked to the paper.

## Dataset profile

| Item           | Count |
|----------------|-------|
| Samples        | 1024  |
| Source records | 128   |
| Tools/domains  | 32    |
| Languages      | 8     |
| Field instances| 5592  |

Each of the 32 public tools/services contributes 4 frozen records; every record
is paired with all 8 language settings, yielding 1,024 samples (64 per language,
16 per domain in each split).

## Languages

Chinese (zh), Japanese (ja), Thai (th), Indonesian (id), Tibetan (bo),
Uyghur (ug), traditional Mongolian (mn-Mong), Arabic-script Kazakh (kk-Arab).

## Per-sample fields

| Field                    | Type   | Description |
|--------------------------|--------|-------------|
| sample_id                | string | Unique sample key, e.g. `crates_io_clap_zh_001` |
| split                    | string | `dev` or `test`; record-disjoint, 512 samples each |
| language                | string | One of the 8 language codes above |
| query                    | string | Target-language user query |
| tool                    | string | Normalized tool name (32 domains) |
| domain                  | string | Domain key, e.g. `crate` |
| tool_result             | object | Frozen static result in JSON-like form |
| required_fields          | list   | Fields the answer must express |
| field_specs             | object | field -> role mapping (authoritative role source) |
| preserve_exact_fields    | list   | Values copied verbatim |
| localizable_fields       | list   | Values with explicit localization requirement |
| forbidden_patterns       | list   | Unsupported addition patterns (hallucination check) |
| source_metadata          | object | provider, documentation URL, request URL, retrieved_at |

## Field roles (authoritative counts from field_specs)

| Role      | Instances |
|-----------|-----------|
| immutable | 1888      |
| entity    | 1376      |
| semantic  | 2008      |
| status    | 320       |

Status is the only role with an explicit localization requirement (320 instances).

## Required-field count distribution

| Required fields | Samples |
|-----------------|---------|
| 4               | 32      |
| 5               | 616     |
| 6               | 280     |
| 7               | 64      |
| 8               | 32      |

## Validation gates

The dataset is accepted only if all of the following hold, checked against the
frozen files in this directory:

1. Total samples == 1024 (across all JSONL files).
2. Exactly 32 distinct domains and 8 distinct language codes.
3. Role-instance counts == table above (1888/1376/2008/320), summing to 5592.
4. Per-sample required-field distribution == table above.
5. dev/test splits are source-record-disjoint with 512 samples each.
6. Every sample passes the schema gate (all fields above present, correct types).

## 32 source domains

air_quality, arxiv_paper, book, clinical_trial, country, crate, crypto_market,
currency_exchange, earthquake, fda_drug_label, food, gbfs_station, geocode,
github, gutenberg, hackernews_item, holiday, indicator, iss_location, music,
npm, postal, pypi, scholarly, species, stackexchange_question, sunrise_sunset,
timezone, university, weather, wikidata, wikipedia.

## File layout

Frozen JSONL files are expected under `data/raw/records_*.jsonl` (or as shipped
by the artifact repository). The fetch script `~/.hermes/scripts/fetch_realtool_loc_data.py`
downloads, validates against the gates above, and commits the result.