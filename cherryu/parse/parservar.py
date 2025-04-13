import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import vartypes


def parse_var(c_lines: list[str], line: str, lineno: int) -> bool:
    if line.startswith("var"):
        match = re.match(r'^var[\t ]+([a-zA-Z_]\w*)[\t ]*:[\t ]*([a-zA-Z_]\w*)[\t ]*=[\t ]*(.+)$', line)
        if match:
            name, type_, value = match.group(1), match.group(2), match.group(3)

            if type_ not in vartypes:
                PanicKeywordError(f"\"{type_}\" is not a defined type.", line, lineno)

            elif not vartypes[type_]:
                PanicSyntaxError(f"\"{type_}\" cannot be used as a type of variable.", line, lineno)

            else:
                cpp_type = vartypes[type_]
                c_lines.append(f"{cpp_type} {name} = {value};")
                return True

    elif line.startswith("un"):
        match = re.match(r'^un[\t ]+var[\t ]+([a-zA-Z_]\w*)[\t ]*:[\t ]*([a-zA-Z_]\w*)[\t ]*=[\t ]*(.+)$', line)
        if match:
            name, type_, value = match.group(1), match.group(2), match.group(3)

            if type_ not in vartypes:
                PanicKeywordError(f"\"{type_}\" is not a defined type.", line, lineno)

            elif not vartypes[type_]:
                PanicSyntaxError(f"\"{type_}\" cannot be used as a type of variable.", line, lineno)

            else:
                cpp_type = vartypes[type_]
                c_lines.append(f"const {cpp_type} {name} = {value};")
                return True

    return False
