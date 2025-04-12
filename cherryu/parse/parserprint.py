import re

from cherryu.panics import PanicSyntaxError


def pars_print(c_lines, line, lineno) -> bool:
    if line.startswith("printnl"):
        match = re.match(r'printnl\("(.+?)"\)', line)

        if match:
            text = match.group(1)
            c_lines.append(f'    printf("{text}\\n");')
        else:
            match = re.match(r'printnl\((-?\d+)\)', line)
            if match:
                c_lines.append(f'    printf("{match.group(1)}\\n");')
            else:
                PanicSyntaxError("Wrong Syntax! \n Corract Syntax -> println(<str>)", line, lineno)

        return True

    elif line.startswith("print"):

        match = re.match(r'print\("(.+?)"\)', line)

        if match:
            text = match.group(1)
            c_lines.append(f'    printf("{text}");')
        else:
            match = re.match(r'print\((-?\d+)\)', line)
            if match:
                c_lines.append(f'    printf("{match.group(1)}");')
            else:
                PanicSyntaxError("Wrong Syntax! \n Corract Syntax -> println(<str>)", line, lineno)
        return True

    else:
        return False
