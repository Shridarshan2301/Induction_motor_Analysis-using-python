# Induction Motor Analysis

This project analyzes an induction motor and produces:
- Summary report (console + report.txt)
- Torque-speed, slip-speed, and efficiency vs output power plots
- Basic unit tests and a CI workflow

Requirements
- Python 3.8+
- Install dependencies:
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Usage
```bash
python induction_motor_analysis_final.py
```
Enter the prompted motor parameters when requested.

Run tests
```bash
pytest -q
```

Notes
- On headless systems, configure matplotlib to use a non-interactive backend or modify the script to save figures to files.
- report.txt will be created in the repository root when the script is run.

License: MIT
