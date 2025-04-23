import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import rettypes, vartypes


def parse_f(c_lines: list[str], line: str, lineno: int, ugly: bool) -> bool:
    if line.strip() == "begin main":
        c_lines.insert(0, "#include <exception>")
        c_lines.insert(0, '#include <iostream>')
        c_lines.append("int main(){")
        c_lines.append("try {")
        return True


    elif line.strip() == "end":

        c_lines.append("} catch (const std::exception& e) {")
        c_lines.append('std::cerr << "[Cherry]ERROR!: " << e.what() << std::endl;')
        c_lines.append("return 1;")
        c_lines.append("}")
        c_lines.append("return 0;")
        c_lines.append("}")
        return True

    if line.startswith("f"):
        match = re.match(r'f[\t ]+([a-zA-Z_]\w*)[\t ]*\((.*?)\)[\t ]*->[\t ]*(\w+)[\t ]*{', line)
        if match:
            name, args, rtype = match.group(1), match.group(2), match.group(3)

            args_ = args.split(',') if args else []
            finargs: list[str] = []

            for arg in args_:
                argtemp = arg.strip().split(':')

                if len(argtemp) != 2:
                    PanicSyntaxError(f"Invalid argument format: '{arg}'", line, lineno)

                varname, vartype = argtemp[0].strip(), argtemp[1].strip()

                if vartype not in vartypes:
                    PanicKeywordError(f"Undefined argument type: '{vartype}'", line, lineno)

                finargs.append(f"{vartypes[vartype]} {varname}")

            if rtype not in rettypes:
                PanicKeywordError(f"Undefined return type: '{rtype}'", line, lineno)

            fcline = f'{rettypes[rtype]} {name}({", ".join(finargs)})' + ' {'
            c_lines.append(fcline + "//parsef1.py")
            return True


    elif line.startswith('}') and not ugly:
        if line == "}":
            c_lines.append("}")
            return True
        match = re.match(r'}[\t ]*elif[\t ]*(.+)[\t ]*\{', line)
        if match:
            c_lines.append("}" + f"else if ({match.group(1)})" + "{")
            return True
        else:
            match = re.match(r'}[\t ]*else[\t ]*\{', line)
            if match:
                c_lines.append("}else{")
                return True
            else:
                PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> elif <condition> { <block> }", line, lineno)

    if line.startswith('return'):
        match = re.match(r'return[\t ]+(.+)', line)

        if match:
            c_lines.append(f'return {match.group(1)};')
            return True
        else:
            PanicSyntaxError(
                "Wrong Syntax! \nCorrect Syntax -> return <any>",
                line,
                lineno
            )


    if line.strip().endswith(';') and not ugly:
        c_lines.append(f'return {line.strip()}')
        return True

    return False
