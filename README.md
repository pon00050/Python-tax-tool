# Python Tax Calculation Tool

## Overview
This project is a **Python-based tax calculation tool** designed to help users compute various aspects of tax returns. The tool incorporates multiple IRS forms, worksheets, and schedules, making it a practical resource for understanding tax rules and automating tax calculations.

The program is modular and scalable, allowing for the addition of new tax forms and rules as needed. It is also a **living documentation** of the developer's journey to master tax preparation and Python programming.

---

## Features/Goals
- **Compute Federal Tax (Form 1040)**:
  - Handles incomes below and above $100,000 using tax tables and tax rate schedules.
- **Dependent Care Credit (Form 2441)**:
  - Calculates credit for qualified childcare expenses.
- **Child Tax Credit (Schedule 8812)**:
  - Accounts for phase-outs and maximum credit limits.
- **Credit Limit Worksheet**:
  - Computes credit limits for various deductions and credits.
- **Dynamic Input Handling**:
  - Reads taxpayer data from JSON files for flexibility.
- **Error Handling**:
  - Handles missing files, invalid inputs, and JSON format errors gracefully.
- **Expandable Design**:
  - Supports adding additional tax forms and schedules over time.

---

## File Structure
```plaintext
tax_calculation_tool/
├── README.md                  # Documentation
├── main.py                    # Entry point of the program
├── taxpayer_information.json  # Sample taxpayer data file
├── modules/                   # Core functionality
│   ├── tax_utils.py           # Tax calculations
│   ├── forms_utils.py         # IRS forms (e.g., Form 2441)
│   ├── schedule_utils.py      # Schedules (e.g., Schedule 8812)
│   ├── worksheet_utils.py     # Worksheets and credit calculations
├── data/                      # Tax tables and rate schedules
│   ├── Complete_Tax_Tables.json  # Tax table for income < $100,000
│   ├── Tax_computations_Line16.json  # Tax rate schedule for income ≥ $100,000
└── tests/                     # Unit tests
    ├── test_tax_utils.py      # Tests for tax calculations
    ├── test_forms_utils.py    # Tests for forms
