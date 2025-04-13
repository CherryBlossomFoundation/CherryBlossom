
def parse_ugly(c_lines: list[str], line: str) -> bool:
    if line.startswith("ugly"):
        code = line[5:].strip()  # "ugly"를 제외한 코드 부분
        c_lines.append(code)  # 그냥 C++ 코드 추가
        return True

    return False
