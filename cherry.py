import os
import subprocess
import shutil
from cherryu.status import *
from cherryu.panics import *
from cherryu.parser import parse_cb_to_c

def compile_c_to_exe(c_file: str, exe_file: str):
    if not shutil.which("gcc"):
        print_panic("ERROR! Cant find gcc. Installing gcc first.")
        sys.exit(-1)
    return subprocess.run(["gcc", c_file, "-o", exe_file])

def compile_cb(cb_file: str):
    exe_file = os.path.splitext(cb_file)[0] + ".exe"
    tmp_c_file = "tmp.c"

    with open(cb_file, "r", encoding="utf-8") as f:
        cb_code = f.read()

    c_code = parse_cb_to_c(cb_code)
    with open(tmp_c_file, "w", encoding="utf-8") as f:
        f.write(c_code)

    print_info("Compiling...")
    result = compile_c_to_exe(tmp_c_file, exe_file)

    if result.returncode == 0:
        print_success(f"Compile Done: {exe_file}")
    else:
        print_panic("Cant Compile")

    os.remove(tmp_c_file)

    print("")
    os.system(exe_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("how to use:")
        print("cherry <.cb file>")
        sys.exit(1)

    cb_path = sys.argv[1]
    compile_cb(cb_path)
