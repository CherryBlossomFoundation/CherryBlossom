import re
from cherryu.panics import PanicSyntaxError


def parse_stem_macro_block(lines: list[str], lineno: int, macros: dict[str, str]) -> int:

    line = lines[lineno].strip()
    match = re.match(r'stem@[\t ]([a-zA-Z_]\w*)[\t ]*=[\t ]*{', line)

    if not match:
        PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> stem@ <name> = { <block> }", line, lineno)

    name = match.group(1)
    block_lines: list[str] = []

    opened = 1

    while opened > 0:
        lineno += 1
        if lineno >= len(lines):
            PanicSyntaxError("Unclosed macro block", line, lineno)

        next_line = lines[lineno].strip()

        if next_line.endswith('{'):
            opened += 1
        if next_line.endswith('}'):
            opened -= 1

        if opened > 0:
            block_lines.append(next_line)

    macros[name] = '\n'.join(block_lines)
    return lineno


def parse_stem_macro_line(line: str, lineno: int, macros: dict[str, str]) -> bool:
    if line.startswith("stem@") and not line.endswith('{'):
        match = re.match(r'stem@[\t ]([a-zA-Z_]\w*)[\t ]*=[\t ]*(.+?)(?=[\t ]*//|$)', line)
        if not match:
            PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> stem@ <name> = <value>", line, lineno)
        name, value = match.group(1), match.group(2)
        macros[name] = value
        return True
    return False


def extract_macros(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    macros: dict[str, str] = {}
    new_lines: list[str] = []

    lineno = 0
    while lineno < len(lines):
        line = lines[lineno].strip()

        if line.startswith("stem@") and line.endswith('{'):
            lineno = parse_stem_macro_block(lines, lineno, macros)
            lineno += 1
            continue


        if parse_stem_macro_line(line, lineno + 1, macros):
            lineno += 1
            continue

        new_lines.append(line)
        lineno += 1

    return new_lines, macros
