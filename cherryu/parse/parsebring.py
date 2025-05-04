import json
import os
import re

from cherryu.panics import PanicSyntaxError, PanicNotDefinedError
from cherryu.status import print_panic


def parse_bring(c_lines: list[str], line: str, lineno: int) -> bool:
    from cherryu.parser import parse_cb_to_cpp

    if line.startswith("cppbring"):
        match = re.match(r'cppbring[\t ]+([a-zA-Z0-9_./]+)', line.strip())
        if match:
            loc = match.group(1)
            c_lines.append(f'#include <{loc}>')
            return True
        else:
            PanicSyntaxError("Invalid cppbring statement", line, lineno)

    if line.startswith("bring"):
        match = re.match(r'bring[\t ]+([a-zA-Z_][\w.]*)', line.strip())
        if match:
            path = match.group(1).replace('.', '/')
            cb_path = f"{path}.cb"


            with open("blossom.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                search_paths = config.get("bring", [])

            search_paths = [os.path.join(p, cb_path) for p in search_paths if os.path.isdir(p)]
            search_paths = [p for p in search_paths if os.path.exists(p)]

            if not search_paths:
                PanicNotDefinedError(f"CB module '{cb_path}' not found in the defined paths", line, lineno)

            target_path = search_paths[0]

            with open(target_path, "r", encoding="utf-8") as f:
                cb_code = f.read()

            imported_cpp = parse_cb_to_cpp(cb_code, match.group(1).replace('.', '_'))
            c_lines.extend(imported_cpp.splitlines())
            return True
        else:
            PanicSyntaxError("Invalid bring statement format", line, lineno)

    return False
