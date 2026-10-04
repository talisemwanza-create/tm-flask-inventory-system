# Inventory Management System - Flask REST API

Small retail inventory system with Flask, external API integration (OpenFoodFacts).

## Features
- CRUD: GET /inventory, POST /inventory, PUT /inventory/<barcode>, DELETE /inventory/<barcode>
- External API: GET /lookup/<barcode>
- CLI interface: cli.py
- Unit tests: test_app.py

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install flask requests
python app.py