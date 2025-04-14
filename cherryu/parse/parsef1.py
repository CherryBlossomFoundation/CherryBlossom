import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import rettypes, vartypes

def parse_f(c_lines: list[str], line: str, lineno: int) -> bool:
    if line.startswith("f"):
        match = re.match(r'f[\t ]+([a-zA-Z_]\w*)[\t ]*\((.*?)\)[\t ]*:[\t ]*(\w+)[\t ]*{', line)
        if match:
            name, args, rtype = match.group(1), match.group(2), match.group(3)

            

            args_ = args.split(',') if args else []
            finargs: list[str] = []

            for arg in args_:
                argtemp = arg.strip().split(':')

                if len(argtemp) != 2:
                    PanicSyntaxError(f"Invalid argument format: '{arg}'", line, lineno)

                vartype, varname = argtemp[0].strip(), argtemp[1].strip()

                if vartype not in vartypes:
                    PanicKeywordError(f"Undefined argument type: '{vartype}'", line, lineno)

                finargs.append(f"{vartypes[vartype]} {varname}")

            if rtype not in rettypes:
                PanicKeywordError(f"Undefined return type: '{rtype}'", line, lineno)

            fcline = f'{rettypes[rtype]} {name}({", ".join(finargs)})' + ' {'
            c_lines.append(fcline)
            return True

    elif line.startswith('}'):
        c_lines.append('}')
        return True

    return False
