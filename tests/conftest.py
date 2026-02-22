"""Pytest configuration for tests."""

import os
import sys

# Set up path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Set DATABASE_URL before any imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
