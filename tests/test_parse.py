import ast
import json
from pathlib import Path
import types

import pytest


# Helper to load only the parse_hedge_fund_response function from src/main.py
def load_parse_function():
    path = Path(__file__).resolve().parents[1] / "src" / "main.py"
    module_ast = ast.parse(path.read_text())
    func_node = None
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == "parse_hedge_fund_response":
            func_node = node
            break
    if func_node is None:
        raise AssertionError("parse_hedge_fund_response not found")

    func_module = ast.Module(body=[func_node], type_ignores=[])
    ns: dict[str, types.FunctionType] = {}
    exec(compile(func_module, filename=str(path), mode="exec"), {"json": json}, ns)
    return ns["parse_hedge_fund_response"]


parse_hedge_fund_response = load_parse_function()


def test_valid_json_returns_dict():
    json_str = '{"a": 1, "b": "two"}'
    result = parse_hedge_fund_response(json_str)
    assert isinstance(result, dict)
    assert result == {"a": 1, "b": "two"}


def test_invalid_json_returns_none():
    invalid_json = '{"a": 1 "b": 2}'  # missing comma
    assert parse_hedge_fund_response(invalid_json) is None


def test_non_string_input_returns_none():
    assert parse_hedge_fund_response({"a": 1}) is None
