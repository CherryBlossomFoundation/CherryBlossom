import re

#WIP!!
def parse_class(line: str, lineno: int, c_lines: list[str], state: dict) -> bool:
    if line.startswith("class"):
        match = re.match(r'class[\t ]+([a-zA-Z_]\w*)[\t ]*{', line)
        if match:
            class_name = match.group(1)
            c_lines.append(f"class {class_name} {{")
            c_lines.append("public:")
            state["in_class"] = True
            return True

    elif line.strip() == "}" and state.get("in_class"):
        c_lines.append("};")
        state["in_class"] = False
        return True

    return False
