import json
import os
import subprocess
import shutil
import sys
from cherryu.status import *
from cherryu.panics import *
from cherryu.parser import parse_cb_to_cpp

version = "1.4.3"


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
    print(f"Version {version}\n")
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
begin main

// type code here!

end
    """

    with open("blossom.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(f"{name}.cb", "w", encoding="utf-8") as f:
        f.write(cbfile)

    print_success("Done!")


def compile_cb(cb_file: str, istoexe: bool = False):
    try:
        with open("blossom.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            name = config.get("name")
            version = config.get("version")
    except (FileNotFoundError, json.JSONDecodeError):
        print_panic("blossom.json not found.\nIf you want to start a project, type cherry --init.")
        sys.exit(1)

    print_info("[Cherry] Compiling")

    with open(cb_file, "r", encoding="utf-8") as f:
        cb_code = f.read()

    cpp_code = parse_cb_to_cpp(cb_code, "")

    os.makedirs("debug", exist_ok=True)
    basename = os.path.basename(cb_file)
    tmp_cpp_file = os.path.join("debug", os.path.splitext(basename)[0] + ".cpp")
    exe_file = os.path.join("debug", name + ".exe")

    with open(tmp_cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_code)

    if istoexe:
        print_info("[Cherry] Build...")
        if not shutil.which("g++"):
            print_panic("ERROR! Can't find g++. Please install g++ first.")
            sys.exit(-1)

        result = subprocess.run(["g++", tmp_cpp_file, f"-DVERSION=\"{version}\"", "-o", exe_file])

        if result.returncode == 0:
            print_success(f"[Cherry] Compile Done!: {exe_file}")

            print_info("[Cherry] Running executable...")
            if os.name == "nt":
                os.system(f'"{exe_file}"')
            else:
                os.system(f"./{exe_file}")

        else:
            print_panic("[Cherry] Can't Compile")
            sys.exit(1)
    else:
        print_success(f"C++ file generated: {tmp_cpp_file}")


def main():
    if len(sys.argv) <= 1:
        print("How to use:")
        print("cherry --init                Initialize new project")
        print(f"cherry --version             Check version")
        print("cherry <file.cb>             Compile and run")
        print("cherry <file.cb> --tocpp     Compile to C++ only")
        sys.exit(1)

    if "--version" in sys.argv:
        print(f"CherryBlossom {version}")
        return

    if len(sys.argv) == 2:
        if sys.argv[1] == "--init":
            if not os.listdir("."):
                initiating()
            else:
                print_panic("Cannot initialize: current folder is not empty.")
                print_info("Please use 'cherry --init' in an empty directory.")
        else:
            cb_path = sys.argv[1]
            compile_cb(cb_path, True)
    else:
        if "--tocpp" in sys.argv:
            cb_path = sys.argv[1]
            compile_cb(cb_path, False)


if __name__ == "__main__":
    main()
