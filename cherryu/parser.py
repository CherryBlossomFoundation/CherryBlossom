import re

from cherryu.panics import PanicSyntaxError, PanicKeywordError, PanicNotDefinedError
from cherryu.parse.parsermacro import extract_macros
from cherryu.parse.parserprint import pars_print


def parse_cb_to_c(cb_code: str) -> str:
    c_lines = ['#include <stdio.h>', '#include <stdint.h>', '', 'int main() {']

    lines, macros = extract_macros(cb_code.splitlines())



    for lineno, line in enumerate(lines, start=1):

        line = apply_macros(line, macros)

        if not line.strip():
            continue

        if pars_print(c_lines, line, lineno):
            continue


        PanicKeywordError("Unknown Keyword", line, lineno)

    c_lines.append('    return 0;')
    c_lines.append('}')
    return '\n'.join(c_lines)

def apply_macros(line: str, macros: dict[str, str]) -> str:
    def replacer(match: re.Match) -> str:
        name = match.group(1)
        if name not in macros:
            PanicNotDefinedError(f"stem @{name} is not defined", line, 0)
        return macros[name]

    return re.sub(r'@([a-zA-Z_]\w*)', replacer, line)

