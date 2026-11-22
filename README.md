# CSV Data Quality

A small standard-library Python tool that profiles any CSV before you trust it:
shape, inferred column types, missing values, distinct counts, duplicate and
ragged rows, numeric stats, and top values for text columns.

## Quick start

```bash
python3 profile_csv.py data/credit_sample.csv
```

Sample output (truncated):

```
File: data/credit_sample.csv
Rows: 5000  Columns: 21
Duplicate rows: 18  Ragged rows: 0

- CheckingStatus [text] missing=0 distinct=4
    top: no_checking (1993), less_0 (1398), 0_to_200 (1304)
- LoanDuration [numeric] missing=0 distinct=59
    min=4.0 max=64.0 mean=21.393 median=21.0
- CreditHistory [text] missing=0 distinct=5
    top: prior_payments_delayed (1686), credits_paid_to_date (1490), outstanding_credit (938)
```

## What it checks

- **Shape** - row and column counts, plus ragged rows whose field count differs
  from the header.
- **Duplicates** - exact duplicate data rows.
- **Per column** - inferred type (numeric or text), missing count, distinct
  count, min/max/mean/median for numerics, and the three most common values
  for text columns.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

7 tests cover shape, duplicate and ragged detection, missing values, type
inference, numeric stats, top values and empty-file handling. The same tests
run in GitHub Actions on every push.

## Sample data

`data/credit_sample.csv` is a fictitious credit-risk training dataset
(5,000 rows, 21 columns) distributed with IBM SkillsBuild data-learning
material and bundled here for practice. It contains no real personal data.
