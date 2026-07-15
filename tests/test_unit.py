from io import StringIO

import progress_table.progress_table as progress_table_module
from progress_table.progress_table import ProgressTable


class InteractiveStringIO(StringIO):
    def isatty(self):
        return True


def test_automatic_interactivity(monkeypatch):
    monkeypatch.delenv("PTABLE_INTERACTIVE", raising=False)
    monkeypatch.delenv("TERM", raising=False)
    monkeypatch.setattr(progress_table_module, "is_ipython_kernel", lambda: False)

    assert ProgressTable(file=StringIO()).interactive == 0
    assert ProgressTable(file=InteractiveStringIO()).interactive == 2
    assert ProgressTable(file=[InteractiveStringIO(), StringIO()]).interactive == 0

    monkeypatch.setenv("TERM", "dumb")
    assert ProgressTable(file=InteractiveStringIO()).interactive == 0


def test_ipython_interactivity_precedes_stream_detection(monkeypatch):
    monkeypatch.delenv("PTABLE_INTERACTIVE", raising=False)
    monkeypatch.setattr(progress_table_module, "is_ipython_kernel", lambda: True)

    assert ProgressTable(file=StringIO()).interactive == 1


def test_explicit_interactivity_precedes_automatic_detection(monkeypatch):
    monkeypatch.setenv("PTABLE_INTERACTIVE", "1")
    monkeypatch.setattr(progress_table_module, "is_ipython_kernel", lambda: True)

    assert ProgressTable(interactive=2, file=StringIO()).interactive == 2
    assert ProgressTable(file=StringIO()).interactive == 1


def test_aggregate_mean():
    table = ProgressTable()
    table.add_column("value", aggregate="mean")
    assert table.column_aggregates["value"].__name__ == "aggregate_mean"

    for i in range(10):
        table["value"] = i

    assert table["value"] == 4.5


def test_aggregate_sum():
    table = ProgressTable()
    table.add_column("value", aggregate="sum")
    assert table.column_aggregates["value"].__name__ == "aggregate_sum"

    for i in range(10):
        table["value"] = i

    assert table["value"] == 45


def test_aggregate_min():
    table = ProgressTable()
    table.add_column("value", aggregate="min")
    assert table.column_aggregates["value"].__name__ == "aggregate_min"

    for i in range(10):
        table["value"] = i

    assert table["value"] == 0


def test_aggregate_max():
    table = ProgressTable()
    table.add_column("value", aggregate="max")
    assert table.column_aggregates["value"].__name__ == "aggregate_max"

    for i in range(10):
        table["value"] = i

    assert table["value"] == 9
