import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import rettypes, vartypes


def parse_def(c_lines: list[str], line: str, lineno: int) -> bool:
    defic = re.match(r'^([a-zA-Z_.][\w.]*)\s*\((.*?)\)\s*$', line.strip())

    retfic = re.match(r'^return\s+([a-zA-Z_.][\w.]*)\s*\((.*?)\)\s*$', line.strip())

    if retfic:
        c_lines.append(f'return {retfic.group(1)}({retfic.group(2)});')
        return True

    elif defic:

        c_lines.append(f'{defic.group(1).replace(".", "_")}({defic.group(2)});')
        return True

    else:
        return False
