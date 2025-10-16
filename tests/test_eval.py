# tests/test_eval.py
# Ensure ../app is on sys.path so we can import app.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

import pytest
from app import safe_eval_arith

def test_simple_add():
    assert safe_eval_arith("2+2") == 4

def test_mult_paren():
    assert safe_eval_arith("3*(4+1)") == 15

def test_power_mod():
    assert safe_eval_arith("2**3 % 3") == (2**3) % 3

def test_unauthorized_name():
    with pytest.raises(ValueError):
        safe_eval_arith("__import__('os').system('ls')")

def test_invalid_syntax():
    with pytest.raises(ValueError):
        safe_eval_arith("2+")
