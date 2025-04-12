import re

vartypes = {
    'i8': 'int8_t',
    'i16': 'int16_t',
    'i32': 'int32_t',
    'i64': 'int64_t',
    'u8': 'uint8_t',
    'u16': 'uint16_t',
    'u32': 'uint32_t',
    'u64': 'uint64_t',
    'bool': '_Bool',
    'f32': 'float',
    'f64': 'double',
    'str': 'char',
    'void': False
}

def parse_var(c_lines:[str], line:str, lineno:int):
    if line.startswith("var"):
        match = re.match(r'^var\s+([a-zA-Z_]\w*)\s*:\s*([a-zA-Z_]\w*)\s*=\s*(.+)$', line)

        if match:

            match.group(1)
