"""Web tests for Theta* (Nash et al., 2007), https://cdn.aaai.org/AAAI/2007/AAAI07-187.pdf.
Programmer: Uzia Peer. Date: 2026-10-12.
"""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "theta_demo", Path(__file__).parents[1] / "app.py"
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


@pytest.fixture
def client():
    module.app.config["TESTING"] = True
    return module.app.test_client()


def payload(**changes):
    data = {
        "action": "run",
        "cells": "0 0\n0 0",
        "sx": 0,
        "sy": 0,
        "gx": 2,
        "gy": 2,
    }
    data.update(changes)
    return data


def test_pages(client):
    assert client.get("/").status_code == 200
    assert client.get("/about").status_code == 200


def test_result_and_logs(client):
    data = payload()
    result = client.post("/", data=data)
    assert result.status_code == 200
    text = result.get_data(as_text=True)
    assert "2.8284" in text and "Found" in text and "<svg" in text
    assert "[(0, 0), (2, 2)]" in text


@pytest.mark.parametrize(
    "field,value",
    [
        ("cells", "0 0\n1"),
        ("cells", "<script>"),
        ("cells", ""),
        ("gx", 99),
        ("sx", "a"),
    ],
)
def test_invalid_input(client, field, value):
    data = payload()
    data[field] = value
    result = client.post("/", data=data)
    assert result.status_code == 400
    assert b"<script>" not in result.data


def test_no_path(client):
    data = payload()
    data.update(cells="0 1 0\n0 1 0", gx=3, gy=0)
    result = client.post("/", data=data)
    assert result.status_code == 200
    assert "אין מסלול" in result.get_data(as_text=True)


def test_map_repeatable_and_does_not_run_algorithm(client):
    data = payload(action="map", width=7, height=4, density=20, seed=123)
    a = client.post("/", data=data)
    b = client.post("/", data=data)
    assert a.status_code == 200 and a.data == b.data
    assert b'value="7"' in a.data
    assert "תוצאת Basic Theta" not in a.get_data(as_text=True)


def test_random_endpoints_are_valid_and_do_not_run_algorithm(client):
    data = payload(action="points", cells="0 0 0\n0 1 0")
    result = client.post("/", data=data)
    assert result.status_code == 200
    text = result.get_data(as_text=True)
    first_values = {
        name: int(re.search(rf'name="{name}" value="(\d+)"', text).group(1))
        for name in ("sx", "sy", "gx", "gy")
    }
    start = first_values["sx"], first_values["sy"]
    goal = first_values["gx"], first_values["gy"]
    grid = module.parse_grid(data["cells"])
    assert (start, goal) != ((0, 0), (2, 2))
    assert start != goal
    assert grid.valid_corner(start) and grid.valid_corner(goal)
    assert "תוצאת Basic Theta" not in text

    second = client.post("/", data=payload(**(data | first_values)))
    second_text = second.get_data(as_text=True)
    second_values = {
        name: int(re.search(rf'name="{name}" value="(\d+)"', second_text).group(1))
        for name in ("sx", "sy", "gx", "gy")
    }
    assert second_values != first_values


def test_oversized(client):
    assert client.post("/", data={"cells": "0" * 60_000}).status_code == 413
