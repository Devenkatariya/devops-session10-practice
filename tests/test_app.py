"""Tests for app module."""
import sys
sys.path.insert(0, 'src')
from app import calculate_deployment_risk

def test_low_risk_deployment():
    """Small change with tests and review = low risk."""
    changes = {
        'files_changed': 2,
        'lines_changed': 30,
        'has_tests': True,
        'has_review': True
    }
    assert calculate_deployment_risk(changes) == 'low'

def test_high_risk_no_review():
    """Any change without review = high risk."""
    changes = {
        'files_changed': 1,
        'lines_changed': 10,
        'has_tests': True,
        'has_review': False  # No review = high risk!
    }
    assert calculate_deployment_risk(changes) == 'high'

def test_high_risk_no_tests_large():
    """Large change without tests = high risk."""
    changes = {
        'files_changed': 25,
        'lines_changed': 600,
        'has_tests': False,
        'has_review': True
    }
    assert calculate_deployment_risk(changes) == 'high'

def test_medium_risk():
    """Medium sized change = medium risk."""
    changes = {
        'files_changed': 8,
        'lines_changed': 150,
        'has_tests': True,
        'has_review': True
    }
    assert calculate_deployment_risk(changes) == 'medium'

print("All tests defined successfully")
