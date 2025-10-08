# KAP - Datenqualität Neurologie

This repository contains the implementation of a configurable data quality pipeline developed within the KAP. It systematically evaluates **completeness**, **conformance**, and **plausibility** of neurological datasets based on configurable rules.

---

## ⚙️ Setup Instructions

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the environment

**On Linux/MacOS:**

```bash
source .venv/bin/activate
```

**On Windows:**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

To run the pipeline using the included example configuration (`config.json`), simply execute:

```bash
python3 main.py
```

If no dataset path is provided, a synthetic test dataframe will be generated automatically.

---

## 🧠 Advanced Usage

### 4.1 Create a new configuration

If no configuration file exists yet, you can generate a template for a specific CSV file using:

```bash
python3 util.py -p path/to/<file>.csv
```

This will create a draft `config.json` including column metadata.  
Next, review and adjust:

- **Datatypes**
- **Expected value ranges**
- **Unit specifications**
- **Column-level checks**

Many basic checks (e.g., uniqueness, completeness, atemporal plausibility, value conformance, simple temporal plausibility) are auto-generated from this configuration.

### 4.2 Run data quality checks

```bash
python3 main.py /path/to/<file>.csv
```

Passing the dataset path is optional — if omitted, the system defaults to the test dataframe.

## 🧾 Example Output

An example result is included in [`example_result.json`](example_result.json).

Below is the CLI output from a simple run using the _Quick Start_ instructions:

```bash
python3 main.py

No path to CSV file provided. Using test data.
------------------------- NOW EXECUTING STAGE 1 CHECKS -------------------------
Executed 1 stage 1 checks.
------------------------- NOW EXECUTING STAGE 2 CHECKS -------------------------
Executed 4 stage 2 checks.
------------------------- NOW EXECUTING STAGE 3 CHECKS -------------------------
Executed 4 stage 3 checks.
------------------------- ALL CHECKS COMPLETED -------------------------
Total number of checks: 9
All checks ran successfully. No failed checks.

Results Stage 1: 1/1 checks executed
Results Stage 2: 4/4 checks executed
Results Stage 3: 4/4 checks executed

Total number of rows in the DataFrame: 1000
Total number of bad IDs: 509
Score: 491 / 1000 → 49.1%

------------------------- EXPORTING RESULTS -------------------------
Results exported to results/results_2025-10-08_15-56.json
------------------------- RESULTS EXPORT COMPLETED -------------------------
```
