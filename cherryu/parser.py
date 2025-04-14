from cherryu.panics import PanicSyntaxError, PanicKeywordError, PanicNotDefinedError
from cherryu.parse.parsermacro import extract_macros
from cherryu.parse.parservar import parse_var
from cherryu.parse.parsef1 import parse_f
from cherryu.parse.parsebring import parse_bring
import re

def parse_cb_to_cpp(cb_code: str) -> str:
    ugly = False
    cpp_lines = [
        '#include <iostream>',
        '#include <string>',
        '#include <cstdint>',
        '#include <stdexcept>',
        ''
    ]

    lines, macros = extract_macros(cb_code.splitlines())
    ugly_depth = 0

    for lineno, line in enumerate(lines, start=1):
        line = apply_macros(line, macros)
        stripped = line.strip()

        if re.match(r'^ugly[\t ]*\{', stripped):
            ugly = True
            ugly_depth = 1
            continue

        if ugly:
            cpp_lines.append(line)
            if '{' in line:
                ugly_depth += line.count('{')
            if '}' in line:
                ugly_depth -= line.count('}')
                if ugly_depth <= 0:
                    ugly = False
            continue

        if not stripped:
            continue

        if parse_bring(cpp_lines, line, lineno):
            continue

        if parse_f(cpp_lines, line, lineno):
            continue

        if parse_var(cpp_lines, line, lineno):
            continue
            
        PanicKeywordError("Unknown Keyword", line, lineno)

    return '\n'.join(cpp_lines)


def apply_macros(line: str, macros: dict[str, str]) -> str:
    def replacer(match: re.Match) -> str:
        name = match.group(1)
        if name not in macros:
            PanicNotDefinedError(f"stem @{name} is not defined", line, 0)
        return macros[name]

    return re.sub(r'@([a-zA-Z_]\w*)', replacer, line)

