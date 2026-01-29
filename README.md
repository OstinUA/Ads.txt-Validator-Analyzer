# AdOps Shield: Ads.txt Validator & Analyzer

A professional tool designed for AdOps teams to automate the validation, analysis, and visualization of `ads.txt` and `app-ads.txt` files. This application parses supply chain data, checks for IAB Tech Lab compliance, and provides actionable insights.

## Features

* **Multi-Source Ingestion:** Load local text files or fetch directly from live domains (auto-detects `app-ads.txt` path).
* **IAB Syntax Validation:** rigorous checking against IAB specifications (detects missing parameters, invalid account types, formatting errors).
* **Analytics Dashboard:** Visualizes `DIRECT` vs `RESELLER` inventory and identifies top supply partners.
* **Data Export:** Convert unstructured text files into clean, structured CSV datasets.

## Tech Stack

* **Python 3.10+**
* **Streamlit:** Web Interface
* **Pandas:** Data Manipulation
* **Plotly:** Interactive Data Visualization
* **Requests:** HTTP Data Fetching

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/ads.txt-validator-analyzer.git](https://github.com/your-username/ads.txt-validator-analyzer.git)
