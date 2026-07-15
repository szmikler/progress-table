#  Copyright (c) 2022-2025 Szymon Mikler
#  Licensed under the MIT License

"""Common utilities for progress_table."""

import os
import sys
from typing import Optional, TextIO, Union

from colorama import Back, Fore, Style

ALL_COLOR_NAME = [x for x in dir(Fore) if not x.startswith("__")]
ALL_STYLE_NAME = [x for x in dir(Style) if not x.startswith("__")]
ALL_COLOR_STYLE_NAME = ALL_COLOR_NAME + ALL_STYLE_NAME
ALL_COLOR = [getattr(Fore, x) for x in ALL_COLOR_NAME] + [getattr(Back, x) for x in ALL_COLOR_NAME]
ALL_STYLE = [getattr(Style, x) for x in ALL_STYLE_NAME]
ALL_COLOR_STYLE = ALL_COLOR + ALL_STYLE

COLORAMA_TRANSLATE = {
    "bold": "bright",
}

NoneType = type(None)
ColorFormat = Union[str, tuple, list, NoneType]
ColorFormatTuple = (str, tuple, list, NoneType)
CURSOR_UP = "\033[A"


def maybe_convert_to_colorama_str(color: str) -> str:
    """Convert color from string to colorama string."""
    color = COLORAMA_TRANSLATE.get(color.lower(), color)

    if isinstance(color, str):
        if hasattr(Fore, color.upper()):
            return getattr(Fore, color.upper())
        if hasattr(Style, color.upper()):
            return getattr(Style, color.upper())

    assert color in ALL_COLOR_STYLE, f"Color {color!r} incorrect! Available: {' '.join(ALL_COLOR_STYLE_NAME)}"
    return color


def maybe_convert_to_colorama(color: ColorFormat) -> str:
    """Fix unintuitive colorama names.

    Translation layer from user-passed to colorama-compatible names.
    """
    if color is None or color == "":
        return ""
    if isinstance(color, str):
        color = color.split(" ")
    results = [maybe_convert_to_colorama_str(x) for x in color]
    return "".join(results)


def is_ipython_kernel() -> bool:
    try:
        from IPython.core.getipython import get_ipython  # pyright: ignore[reportMissingImports]

        ipython = get_ipython()
        if ipython is not None:
            return "IPKernelApp" in ipython.config
        return False
    except ImportError:
        return False


def is_interactive_terminal(stream: Optional[TextIO] = None) -> bool:
    """Check whether a stream supports interactive terminal output."""
    if stream is None:
        stream = sys.stdout
        assert stream is not None
    try:
        return stream.isatty() and os.environ.get("TERM") != "dumb"
    except (AttributeError, OSError, ValueError):
        return False
