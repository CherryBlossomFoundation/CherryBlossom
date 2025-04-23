import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import vartypes

def parse_keyword(c_lines: list[str], line: str, lineno: int, nestedvarnum: int) -> bool:
    if line.strip() in vartypes:
        c_lines.append(vartypes[line.strip()])
        return True

    if line.startswith("if"):
        match = re.match(r'if[\t ]*(.+)[\t ]*\{', line)
        if match:
            c_lines.append(f"if ({match.group(1)})" + "{")
            return True
        else:
            PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> if <condition> { <block> }", line, lineno)

    if line.startswith("elif"):
        match = re.match(r'elif[\t ]*(.+)[\t ]*\{', line)
        if match:
            c_lines.append(f"else if ({match.group(1)})" + "{")
            return True
        else:
            PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> elif <condition> { <block> }", line, lineno)


    if line.startswith("else"):
        match = re.match(r'else[\t ]*\{', line)
        if match:
            c_lines.append("else{")
            return True
        else:
            PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> else { <block> }", line, lineno)

    if line.startswith("cycle"):
        match = re.match(r'cycle[\t ]*\{', line)

        if match:
            nestedvarnum += 1
            c_lines.append(f'int i{nestedvarnum} = 0;')
            c_lines.append('while (true){')
            c_lines.append(f'i{nestedvarnum}++;')
            return True
        else:
            match = re.match(r'cycle[\t ]+([0-9]+)[\t ]*{', line)

            if match:
                nestedvarnum += 1
                c_lines.append(f'int i{nestedvarnum} = 0;')
                c_lines.append(f"while (i{nestedvarnum}<{int(match.group(1))})" + '{')
                c_lines.append(f'i{nestedvarnum}++;')
                return True
            else:
                match = re.match(r'cycle[\t ]+(.+)[\t ]*{', line)

                if match:
                    c_lines.append(f'int i{nestedvarnum} = 0;')
                    c_lines.append(f'while ({match.group(1)}) ' + '{')
                    c_lines.append(f'i{nestedvarnum}++;')

                else:
                    PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> cycle <none|time|condition> { <block> }", line, lineno)


    if line.startswith("for"):
        match = re.match(r'for[\t ]+(.+),[\t ]*(.+),[\t ]*(.+)[\t ]*{', line)
        if match:
            init = match.group(1)
            cond = match.group(2)
            step = match.group(3)
            c_lines.append(f'for ({init}; {cond}; {step}) {{')
            return True
        else:
            PanicSyntaxError(
                "Wrong Syntax! \nCorrect Syntax -> for <init>, <condition>, <step> { <block> }",
                line,
                lineno
            )

