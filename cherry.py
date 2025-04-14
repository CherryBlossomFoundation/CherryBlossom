import os
import subprocess
import shutil
import sys
from cherryu.status import *
from cherryu.panics import *
from cherryu.parser import parse_cb_to_cpp


def compile_cpp_to_exe(cpp_file: str, exe_file: str):
    if not shutil.which("g++"):
        print_panic("ERROR! Can't find g++. Installing g++ first.")
        sys.exit(-1)

    return subprocess.run(["g++", cpp_file, "-o", exe_file])


def compile_cb(cb_file: str, istoexe: bool = False):
    exe_file = os.path.splitext(cb_file)[0] + ".exe"
    tmp_cpp_file = "tmp.cpp"

    # .cb 파일 읽기
    with open(cb_file, "r", encoding="utf-8") as f:
        cb_code = f.read()

    # Cherry Blossom 코드를 C++로 변환
    cpp_code = parse_cb_to_cpp(cb_code)

    # C++ 코드 파일로 저장
    with open(tmp_cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_code)

    # 컴파일
    print_info("Compiling...")
    result = compile_cpp_to_exe(tmp_cpp_file, exe_file)

    if result.returncode == 0:
        print_success(f"Compile Done: {exe_file}")
    else:
        print_panic("Can't Compile")

    os.remove(tmp_cpp_file)

    print("")
    os.system(exe_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("How to use:")
        print("cherry <.cb file>")
        sys.exit(1)
    if len(sys.argv) >= 2:
        cb_path = sys.argv[1]
        compile_cb(cb_path, True)
    else:
        cb_path = sys.argv[1]

        compile_cb(cb_path)


