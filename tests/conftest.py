from __future__ import annotations

import copy

import pytest

from pluralio import registry


@pytest.fixture(autouse=True)
def _isolate_registry():
    backup = copy.deepcopy(registry._REGISTRY)
    yield
    registry._REGISTRY = backup
