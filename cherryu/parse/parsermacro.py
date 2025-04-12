import re
from cherryu.panics import PanicSyntaxError

#이건 너무 개념이 어려워서 챗황한테 도와달라 해씀
def parse_stem_macro_block(lines: list[str], lineno: int, macros: dict[str, str]) -> int:
    """
    stem@ name = { ... } 블록 형태의 매크로를 파싱합니다.
    블록이 닫힐 때까지 줄을 읽고 macros 딕셔너리에 저장합니다.
    반환값은 마지막으로 읽은 줄 번호입니다.
    """
    line = lines[lineno].strip()
    match = re.match(r'stem@\s([a-zA-Z_]\w*)\s*=\s*{', line)

    if not match:
        PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> stem@ <name> = { <block> }", line, lineno)

    name = match.group(1)
    block_lines: list[str] = []

    opened = 1

    while opened > 0:
        lineno += 1
        if lineno >= len(lines):
            PanicSyntaxError("Unclosed macro block", line, lineno)

        next_line = lines[lineno].strip()

        if next_line.endswith('{'):
            opened += 1
        if next_line.endswith('}'):
            opened -= 1

        if opened > 0:
            block_lines.append(next_line)

    macros[name] = '\n'.join(block_lines)
    return lineno


def parse_stem_macro_line(line: str, lineno: int, macros: dict[str, str]) -> bool:
    """
    stem@ name = value 형태의 단일 라인 매크로 파싱.
    성공 시 True 반환, 아니면 False.
    """
    if line.startswith("stem@") and not line.endswith('{'):
        match = re.match(r'stem@\s([a-zA-Z_]\w*)\s*=\s*(.+?)(?=\s*//|$)', line)
        if not match:
            PanicSyntaxError("Wrong Syntax! \nCorrect Syntax -> stem@ <name> = <value>", line, lineno)
        name, value = match.group(1), match.group(2)
        macros[name] = value
        return True
    return False


def extract_macros(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    """
    전체 코드에서 매크로를 먼저 추출합니다.
    나머지 줄은 일반 코드로 반환.
    """
    macros: dict[str, str] = {}
    new_lines: list[str] = []

    lineno = 0
    while lineno < len(lines):
        line = lines[lineno].strip()

        # 블록 매크로
        if line.startswith("stem@") and line.endswith('{'):
            lineno = parse_stem_macro_block(lines, lineno, macros)
            lineno += 1
            continue

        # 단일 줄 매크로
        if parse_stem_macro_line(line, lineno + 1, macros):
            lineno += 1
            continue

        new_lines.append(line)
        lineno += 1

    return new_lines, macros
