from __future__ import annotations
import builtins
from contextlib import contextmanager

def print_boxed_title(text: str) -> None:
    padding = 2
    content = f"{' ' * padding}{text}{' ' * padding}"
    line = "=" * len(content)
    print("\n" + line)
    print(content.center(len(line)))
    print(line)


def print_subtitle(text: str) -> None:
    indent = 2
    prefix = ' ' * indent
    line = '-' * len(text)
    print(f"\n{prefix}{text}")
    print(f"{prefix}{line}")


@contextmanager
def _indent_print(prefix: str):
    original_print = builtins.print

    def wrapped_print(*args, **kwargs):
        sep = kwargs.pop('sep', ' ')
        end = kwargs.pop('end', '\n')
        file = kwargs.pop('file', None)
        flush = kwargs.pop('flush', False)
        text = sep.join(str(a) for a in args)
        # Maneje contenido de varias líneas sangrando cada línea
        lines = text.splitlines() if text else ['']
        indented = '\n'.join(prefix + line if line else prefix.rstrip() for line in lines)
        original_print(indented, end=end, file=file, flush=flush)

    builtins.print = wrapped_print
    try:
        yield
    finally:
        builtins.print = original_print


@contextmanager
def subtitle_block(text: str | None = None, indent: int = 2):
    if text:
        print_subtitle(text)
    prefix = ' ' * indent
    with _indent_print(prefix):
        yield