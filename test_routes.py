#!/usr/bin/env python
"""Test script to verify routes are working"""
import sys
sys.path.insert(0, '.')

from app.routes import main
from flask import Flask

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.register_blueprint(main)

routes = []
for rule in app.url_map.iter_rules():
    if 'static' not in rule.rule:
        routes.append(str(rule.rule))

print(f"✓ Total routes registered: {len(routes)}\n")
print("Routes containing 'export' or 'performance':")
for route in sorted(routes):
    if 'export' in route or 'performance' in route or 'csv' in route:
        print(f"  - {route}")

print("\nAll routes:")
for route in sorted(routes):
    print(f"  - {route}")
