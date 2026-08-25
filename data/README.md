# Data

Frozen benchmark dataset for RealTool-Loc: faithful multilingual realization of
tool results (1,024 tasks, 128 source records, 32 public tools, 8 language
settings).

| File       | Status | Description |
|------------|--------|-------------|
| SCHEMA.md  | ✅     | Field-level dataset specification and validation gates |
| raw/       | ⏳     | Frozen JSONL records — auto-fetched from the artifact repository when it becomes reachable |

### How the data gets here

The paper's artifact repository (`https://anonymous.4open.science/r/RealTool-Loc-46A3`)
hosts the frozen benchmark. A watchdog script
(`~/.hermes/scripts/fetch_realtool_loc_data.py`) probes it on a schedule; once
reachable, it downloads the JSONL files, validates them against SCHEMA.md
(1024 samples, role counts 1888/1376/2008/320, record-disjoint splits), and
commits the result automatically. Until then `raw/` stays empty by design rather
than shipping placeholder or reconstructed data.

### Integrity

Every file landing in `raw/` passes the validation gates defined in SCHEMA.md;
a failing download is never committed. The dataset is static: records are
frozen, and any revision (prompt, records, roles, scoring) increments a version
identifier instead of mutating existing files.