import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError
from .type import rettypes, vartypes


def parse_def(c_lines: list[str], line: str, lineno: int) -> bool:
    # 일반 함수 호출: hello(arg1, arg2)
    defic = re.match(r'^([a-zA-Z_]\w*)[\t ]*\((.*?)\)[\t ]*$', line)

    # return 함수 호출: return hello(arg1, arg2);
    retfic = re.match(r'^return[\t ]+([a-zA-Z_]\w*)[\t ]*\((.*?)\)[\t ]*$', line)

    if retfic:
        c_lines.append(f'return {retfic.group(1)}({retfic.group(2)});')
        return True

    elif defic:
        c_lines.append(f'{defic.group(1)}({defic.group(2)});')
        return True

    else:
        return False
