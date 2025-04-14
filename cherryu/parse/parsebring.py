import os
import re
from cherryu.panics import PanicSyntaxError, PanicKeywordError, PanicNotDefinedError
from cherryu.parser import parse_cb_to_cpp  # 재귀 파싱을 위해 필요


def parse_bring(c_lines: list[str], line: str, lineno: int) -> bool:
    if line.startswith("bring"):
        match = re.match(r'bring[\t ]+([a-zA-Z_][\w.]*)', line.strip())
        if match:
            path = match.group(1).replace('.', '/')
            cb_path = f"{path}.cb"

            if not os.path.exists(cb_path):
                PanicNotDefinedError(f"CB module '{cb_path}' not found", line, lineno)

            with open(cb_path, "r", encoding="utf-8") as f:
                cb_code = f.read()

            imported_cpp = parse_cb_to_cpp(cb_code)
            c_lines.extend(imported_cpp.splitlines())
            return True
        else:
            PanicSyntaxError("Invalid bring statement format", line, lineno)

    return False
