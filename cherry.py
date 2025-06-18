import json
import os
import subprocess
import shutil
import sys
from cherryu.status import *
from cherryu.panics import *
from cherryu.parser import parse_cb_to_cpp

version = "1.4.0"


def initiating():
    print(
        """
   _____   _                                      ____    _                                               
  / ____| | |                                    |  _ \  | |                                              
 | |      | |__     ___    ___   _ __   _   _    | |_) | | |  ___    ___    ___   ___    ___    _ __ ___  
 | |      | '_ \   / _ \  / _ \ | '__| | | | |   |  _ <  | | / __|  / _ \  / __| / __|  / _ \  | '_ ` _ \ 
 | |____  | | | | |  __/ |  __/ | |    | |_| |   | |_) | | | \__ \ | (_) | \__ \ \__ \ | (_) | | | | | | |
  \_____| |_| |_|  \___|  \___| |_|     \__, |   |____/  |_| |___/  \___/  |___/ |___/  \___/  |_| |_| |_|  
                                         __/ |                                                            
                                        |___/                                                             
        """
    , end="")
    print("Version " + version, end="\n\n")
    name = input("Type Project name:")
    exeversion = input("Type Version:")
    defcomppath = os.environ.get("cb_path", "")

    data = {
        "name": name,
        "version": exeversion,
        "bring": [
            defcomppath,
        ]
    }

    cbfile = """
f main() -> int {
    // type code here!
    return 0;
}
    """

    with open("blossom.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(f"{name}.cb", "w", encoding="utf-8") as f:
        f.write(cbfile)

    print_success("Done!")


def generate_cpp(cb_file: str) -> str:
    with open("blossom.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    name = config.get("name")
    if not name:
        print_panic("Project name is missing in blossom.json.")
        sys.exit(1)
def compile_cb(cb_file: str, istoexe: bool = False):
    try:
        with open("blossom.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            name = config.get("name")
            version = config.get("version")
    except (FileNotFoundError, json.JSONDecodeError):
        print_panic("blossom.json not found.\nIf you want to start a project, type cherry --init.")

    print_info("[Cherry] Compiling")
    exe_file = "debug/" + name + ".exe"
    tmp_cpp_file = "debug/" + os.path.splitext(cb_file)[0] + ".cpp"

    with open(cb_file, "r", encoding="utf-8") as f:
        cb_code = f.read()

    cpp_code = parse_cb_to_cpp(cb_code, "")

    os.makedirs("debug", exist_ok=True)
    basename = os.path.basename(cb_file)
    tmp_cpp_file = os.path.join("debug", os.path.splitext(basename)[0] + ".cpp")

    with open(tmp_cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_code)

    return tmp_cpp_file, name


def build_exe(cpp_file: str, exe_name: str, version: str) -> str:
    exe_file = os.path.join("debug", exe_name + ".exe")

    if not shutil.which("g++"):
        print_panic("ERROR! Can't find g++. Please install g++ first.")
        sys.exit(-1)

    print_info("[Cherry] Build...")
    result = subprocess.run(["g++", cpp_file, f"-DVERSION=\"{version}\"", "-o", exe_file])

    if result.returncode == 0:
        print_success(f"[Cherry] Compile Done!: {exe_file}")
        return exe_file
    else:
        print_panic("[Cherry] Can't Compile")
        sys.exit(1)


def run_exe(exe_file: str):
    print_info("[Cherry] Running executable...")
    if os.name == 'nt':  # Windows
        os.system(f'"{exe_file}"')
    else:
        os.system(f"./{exe_file}")


def compile_cb(cb_file: str, istoexe: bool = False):
    try:
        with open("blossom.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            version = config.get("version", "0.0.0")
    except (FileNotFoundError, json.JSONDecodeError):
        print_panic("blossom.json not found or invalid.\nIf you want to start a project, type cherry --init.")
        sys.exit(1)

    print_info("[Cherry] Compiling")
    cpp_file, name = generate_cpp(cb_file)

    if istoexe:
        exe_file = build_exe(cpp_file, name, version)
        run_exe(exe_file)
    else:
        print_success(f"[Cherry] Generated C++ code at {cpp_file}")


def main():
    if len(sys.argv) <= 1:
        print("How to use:")
        print("cherry --init                Initialize new project")
        print(f"cherry --version             Chack version")
        print("cherry <file.cb>             Compile and run")
        print("cherry <file.cb> --tocpp     Compile to C++ only")
        sys.exit(1)

    
    if "--version" in args:
        print(f"CherryBlossom {version}")
        return


    args = sys.argv[1:]

    if len(sys.argv) == 2:
        if "init" in sys.argv:

            if not os.listdir("."):
                initiating()
            else:
                print_panic("Cannot initialize: current folder is not empty.")
                print_info("Please use 'cherry init' in an empty directory.")


    if "--init" in args:
        if not os.listdir("."):
            initiating()
        else:
            print_panic("Cannot initialize: current folder is not empty.")
            print_info("Please use 'cherry --init' in an empty directory.")
        return

    cb_path = next((arg for arg in args if arg.endswith(".cb")), None)
    if not cb_path:
        print_panic("No .cb file specified.")
        return


    if "--tocpp" in args:
        compile_cb(cb_path, istoexe=False)
    else:

        compile_cb(cb_path, istoexe=True)

        if "build" in sys.argv:
            cb_path = sys.argv[1]
            compile_cb(cb_path)



if __name__ == "__main__":
    main()
