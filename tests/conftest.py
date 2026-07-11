from __future__ import annotations

import copy
from collections.abc import Iterator

import pytest

from pluralio import registry


@pytest.fixture(autouse=True)
def _isolate_registry() -> Iterator[None]:
    backup = copy.deepcopy(registry._REGISTRY)
    yield
    registry._REGISTRY = backup
