import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import rettypes, vartypes


def parse_def(c_lines: list[str], line: str, lineno: int) -> bool:
    defic = re.match(r'([a-zA-Z_]\w*)[\t ]*\((.*?)\)', line)
    retfic = re.match(r'([a-zA-Z_]\w*)[\t ]*\((.*?)\)[\t ]*;', line)
    if defic:
        c_lines.append(f'{defic.group(1)}({defic.group(2)});')
        return True
    elif retfic:
        c_lines.append(f'return {defic.group(1)}({defic.group(2)});')
        return True
    else:
        return False