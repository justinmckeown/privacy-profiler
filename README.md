# 🔐 Privacy Profiler

Privacy Profiler is a modular, command-line tool for analyzing the privacy risk of tabular datasets. It computes column- and row-level metrics to help assess re-identification risk and guide anonymization efforts.

---

## 🚀 Features

- 📊 Supports multiple input formats: CSV, Parquet, Excel, JSON
- 🧮 Built-in privacy metrics:
  ### Column-Level
  - Gini Coefficient
  - Shannon Entropy
  - Uniqueness Ratio
  - Null Ratio

  ### Row-Level (Quasi-Identifier Based)
  - k-Anonymity
  - l-Diversity
  - t-Closeness (TVD-based)
  - Mutual Information (inference risk)
  - Minimum Description Length (compressibility)

- 🧠 Interpretation engine:
  - Per-column and per-metric risk classification
  - Includes supporting statistics (min k, MI bits, compression ratio, etc.)
- 🔎 Row-level uniqueness summary (percent uniquely identifiable records)
- 🔁 Flexible architecture (no hardcoded column names)
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

- gini_coefficient: Inequality/skew in value distribution
- shannon_entropy: Diversity or unpredictability
- uniqueness_ratio: Fraction of unique values
- null_ratio: Fraction of missing values

### Row-Level Metrics

- k_anonymity: Smallest equivalence class (low k = high risk)
- l_diversity: Sensitive value diversity within groups
- t_closeness: How closely each group reflects global sensitive value distribution
- mutual_information: Linkage power between QIs and sensitive attribute
- minimum_description_length: Compressibility of QI columns

### Interpretation Output

- Human-readable risk summaries for each metric
- Justified with supporting statistics:
   - "Minimum k is 1; 72% of groups violate k=5; Avg k: 2.1"

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
    ├── model/           # Data loading + runner integration
    ├── metrics/         # All column and row metric logic
    ├── presenter/       # CLI coordinator
    ├── interface/       # Output formatting
    ├── interpreter/     # Interpretation engine
    ├── reporting/       # JSON & CSV exporters
    ├── main.py          # CLI entry point

```

---

## ✅ Roadmap

- [x] CLI tool with privacy metrics
- [x] Row-level uniqueness scoring
- [x] CSV & JSON output
- [ ] Configurable quasi-identifiers + sensitive attribute
- [ ] YAML-based config
- [ ] Full CSV reporting for spreadsheets

---

## 📄 License

GNU AGPLv3 © Justin McKeown
