from cherryu.panics import PanicSyntaxError, PanicKeywordError, PanicNotDefinedError
from cherryu.parse.parsermacro import extract_macros
from cherryu.parse.parseugly import parse_ugly
from cherryu.parse.parservar import parse_var
import re

def parse_cb_to_cpp(cb_code: str) -> str:
    cpp_lines = [
        '#include <iostream>',
        '#include <string>',
        '#include <cstdint>',
        '#include <stdexcept>',
        '',
        'int main() {',
        '    try {'
    ]

    lines, macros = extract_macros(cb_code.splitlines())

    for lineno, line in enumerate(lines, start=1):
        line = apply_macros(line, macros)

        if not line.strip():
            continue

        if parse_ugly(cpp_lines, line):
            continue

        if parse_var(cpp_lines, line, lineno):
            continue

        PanicKeywordError("Unknown Keyword", line, lineno)

    cpp_lines.append('        return 0;')
    cpp_lines.append('    } catch (const std::exception& e) {')
    cpp_lines.append('        std::cerr << "CherryBlossom Runtime Error: " << e.what() << std::endl;')
    cpp_lines.append('        return 1;')
    cpp_lines.append('    }')
    cpp_lines.append('}')

    return '\n'.join(cpp_lines)


def apply_macros(line: str, macros: dict[str, str]) -> str:
    def replacer(match: re.Match) -> str:
        name = match.group(1)
        if name not in macros:
            PanicNotDefinedError(f"stem @{name} is not defined", line, 0)
        return macros[name]

    return re.sub(r'@([a-zA-Z_]\w*)', replacer, line)

