# 🔐 Privacy Profiler

Privacy Profiler is a modular, command-line tool for analyzing the privacy risk of tabular datasets. It computes column- and row-level metrics to help assess re-identification risk and guide anonymization efforts.

---

## 🚀 Features

- 📊 Supports multiple input formats: CSV, Parquet, Excel, JSON
- 🧮 Built-in privacy metrics:
  - Gini Coefficient
  - Shannon Entropy
  - Uniqueness Ratio
  - Null Ratio
- 🧠 Interpretation engine with per-column risk assessments
- 🔎 Row-level uniqueness scoring (k-anonymity-style)
- 🧾 Multi-format output:
  - JSON (metrics, interpretation, full)
  - CSV (flat table for spreadsheet use)
- 🧰 Clean CLI interface with verbose mode
- 🧱 Modular codebase (MVP architecture + SOLID principles)

---

## 📦 Installation

1. Clone this repository:

```bash
git clone https://github.com/your-username/privacy-profiler.git
cd privacy-profiler
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate   # macOS/Linux
```

3. Install dependencies:

```bash
pip install -e .
```

Make sure `pyarrow` or `fastparquet` is installed if you want Parquet support.

---

## 🧪 Example Usage

```bash
privacy-profiler --input data-input/mixed_data.csv --output-format json --output-path data-output/report.json
```

Outputs:

```
data-output/
├── report_metrics.json
├── report_interpretation.json
├── report_full.json
└── report_report.csv
```

---

## 🧠 Output Explained

### Column Metrics

- `gini_coefficient`: Measures inequality in distribution
- `shannon_entropy`: Measures diversity/unpredictability
- `uniqueness_ratio`: % of values that are unique
- `null_ratio`: % of missing values

### Row-Level Risk Summary

- Based on uniqueness across selected quasi-identifiers
- Reports % of unique rows and assigns a risk level

---

## ⚙️ CLI Options

| Flag              | Description                                           |
|-------------------|-------------------------------------------------------|
| `--input` / `-i`   | Input file path (.csv, .parquet, .xlsx, .json)       |
| `--output-format` | Output format: `text` or `json`                       |
| `--output-path`   | Prefix for saved output files                         |
| `--verbose`       | Show metric definitions and summaries                 |
| `--log-level`     | Logging verbosity: DEBUG, INFO, WARNING, ERROR        |

---

## 📂 Project Structure

```
src/
└── privacy_profiler/
    ├── model/           # Data loading + profiling
    ├── metrics/         # Gini, entropy, uniqueness, row risk
    ├── presenter/       # CLI flow control
    ├── interface/       # Output formatting
    ├── reporting/       # JSON & CSV report writing
    ├── main.py          # CLI entry point
```

---

## ✅ Roadmap

- [x] CLI tool with privacy metrics
- [x] Row-level uniqueness scoring
- [x] CSV & JSON output
- [ ] Configurable quasi-identifiers

---

## 📄 License

GNU AGPLv3 © Justin McKeown
