# Progress Table

[![PyPi version](https://img.shields.io/badge/dynamic/json?label=latest&query=info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fprogress-table%2Fjson)](https://pypi.org/project/progress-table)
[![PyPI license](https://img.shields.io/badge/dynamic/json?label=license&query=info.license&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fprogress-table%2Fjson)](https://github.com/szmikler/progress-table/blob/main/LICENSE.txt)
[![codecov](https://codecov.io/gh/szmikler/progress-table/graph/badge.svg?token=CDJKF0FFAQ)](https://codecov.io/gh/szmikler/progress-table)

Lightweight utility to display the progress of your process as a pretty table in the command line.

* Alternative to TQDM whenever you want to track metrics produced by your process
* Designed to monitor ML experiments, but works for any metrics-producing process
* Allows you to see at a glance what's going on with your process
* Increases readability and simplifies your command line logging
* Is efficient: redraws only the modified rows

### Change this:

![example](images/progress-before3.gif)

### Into this:

![example](images/progress-after4.gif)

## Examples

From `examples/` directory:

* Neural network training

![example-training](images/examples-training.gif)

* Progress of multi-threaded downloads

![example-download](images/examples-download.gif)

* Simulation and interactive display of Brownian motion

![example-brown2d](images/examples-brown2d.gif)

* Display of a game board

![example-tictactoe](images/examples-tictactoe.gif)

## Quick start code

```python
import random
import time

from progress_table import ProgressTable

# Create table object:
table = ProgressTable(num_decimal_places=1)

# You can (optionally) define the columns at the beginning
table.add_column("x", color="bold red")

for step in range(10):
    x = random.randint(0, 200)

    # You can add entries in a compact way
    table["x"] = x

    # Or you can use the update method
    table.update("x", value=x, weight=1.0)

    # Display the progress bar by wrapping an iterator or an integer
    for _ in table(10):  # -> Equivalent to `table(range(10))`
        # Set and get values from the table
        table["y"] = random.randint(0, 200)
        table["x-y"] = table["x"] - table["y"]
        table.update("average x-y", value=table["x-y"], weight=1.0, aggregate="mean")
        time.sleep(0.1)

    # Go to the next row when you're ready
    table.next_row()

# Close the table when it's finished
table.close()

```

> Go to [integrations](docs/integrations.md)
> page to see examples of integration with deep learning libraries.

## Advanced usage

Go to [advanced usage](docs/advanced-usage.md) page for more information.

## Troubleshooting

### Excessive output

Progress Table works correctly in most consoles, but there are some exceptions:

* Some cloud logging consoles (e.g. Kubernetes) do not handle live, carriage-return-based redraws properly. You can still use ProgressTable with `interactive=0`. This mode prints rows when they are finalized and does not display progress bars.

* Some consoles, such as the PyCharm Python Console or IDLE, do not support moving the cursor to previous lines. You can still use ProgressTable with `interactive=1`. This mode can redraw the current line and display one progress-bar position, but previous rows remain visually frozen.

> When `interactive` is omitted, it defaults to `1` in Jupyter, `0` when output is redirected, and `2` in an interactive terminal. Set it explicitly when creating the table, or override the automatic default with the `PTABLE_INTERACTIVE` environment variable, for example `PTABLE_INTERACTIVE=1`.

### Other problems

If you encounter different messy outputs or other unexpected behavior: please create an issue!

## Installation

Install Progress Table easily with pip:

```
pip install progress-table
```

## Links

* [See on GitHub](https://github.com/szmikler/progress-table)
* [See on PyPI](https://pypi.org/project/progress-table)

## Alternatives

* Progress bars: great for tracking progress, but they don't provide ways to display data in clear and compact way
    * `tqdm`
    * `rich.progress`
    * `keras.utils.Progbar`

* Libraries displaying data: great for presenting tabular data, but they lack the progress tracking aspect
    * `rich.table`
    * `tabulate`
    * `texttable`
