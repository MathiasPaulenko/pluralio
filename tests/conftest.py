from __future__ import annotations

from collections.abc import Iterator

import pytest

from pluralio import registry


@pytest.fixture(autouse=True)
def _isolate_registry() -> Iterator[None]:
    backup = registry.snapshot()
    yield
    registry.restore(backup)
