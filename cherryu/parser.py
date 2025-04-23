from cherryu.panics import PanicSyntaxError, PanicKeywordError, PanicNotDefinedError
from cherryu.parse.parseclass import parse_class
from cherryu.parse.parsermacro import extract_macros
from cherryu.parse.parservar import parse_var
from cherryu.parse.parsef1 import parse_f
from cherryu.parse.parsebring import parse_bring
from cherryu.parse.parsecodedef import parse_def
from cherryu.parse.parsekeyword import parse_keyword
import re


def parse_cb_to_cpp(cb_code: str) -> str:
    ugly = False
    cpp_lines = [
        '//cb',

    ]
    nestedVarNum = 0
    lines, macros = extract_macros(cb_code.splitlines())
    ugly_depth = 0
    state = {"in_class": False}

    for lineno, line in enumerate(lines, start=1):
        line = apply_macros(line, macros)
        line = strip_comment(line)
        line = line.strip()

        if not line:
            continue

        if re.match(r'^ugly[\t ]*\{', line):
            ugly = True
            ugly_depth = 1
            continue

        if ugly:
            if '{' in line:
                ugly_depth += line.count('{')
                continue
            elif '}' in line:
                ugly_depth -= line.count('}')
                if ugly_depth <= 0:
                    ugly = False
                continue
            else:
                cpp_lines.append(line)
                continue

        if parse_class(line, lineno, cpp_lines, state):
            continue

        if parse_f(cpp_lines, line, lineno, ugly):
            continue

        if parse_bring(cpp_lines, line, lineno):
            continue

        if parse_var(cpp_lines, line, lineno):
            continue

        if parse_def(cpp_lines, line, lineno):
            continue

        if parse_keyword(cpp_lines, line, lineno, nestedVarNum):
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


def strip_comment(line: str) -> str:
    return line.split("//")[0].rstrip()
