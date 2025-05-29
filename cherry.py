import json
import os
import subprocess
import shutil
import sys
from cherryu.status import *
from cherryu.panics import *
from cherryu.parser import parse_cb_to_cpp


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
    print("Version 1.3.0", end="\n\n")
    name = input("Type Project name:")
    exeversion = input("Type Version:")
    defcomppath = os.environ.get("cb_path")

    data = {
        "name": name,
        "version": exeversion,
        "bring": [
            defcomppath,
        ]
    }

    cbfile = """
begin main
    
//type code here!
    
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

    print_info("[Cherry] Compiling")
    os.makedirs("debug", exist_ok=True)
    exe_file = "debug/" + name + ".exe"
    tmp_cpp_file = "debug/" + os.path.splitext(cb_file)[0] + ".cpp"

    with open(cb_file, "r", encoding="utf-8") as f:
        cb_code = f.read()


    cpp_code = parse_cb_to_cpp(cb_code, "")

    with open(tmp_cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_code)

    if istoexe:
        print_info("[Cherry] Build...")
        if not shutil.which("g++"):
            print_panic("ERROR! Can't find g++. Installing g++ first.")
            sys.exit(-1)

        result = subprocess.run(["g++", tmp_cpp_file, f"-DVERSION=\"{version}\"", "-o", exe_file])

        if result.returncode == 0:
            print_success(f"[Cherry] Compile Done!: {exe_file}")


            print("")
            os.system(exe_file)


        else:
            print_panic("[Cherry] Can't Compile")


def main():
    if len(sys.argv) <= 1:
        print("How to use:")
        print("cherry <file.cb>             Compile and run")
        print("cherry <file.cb> --tocpp     Compile to C++ only")
        print("cherry --init                Initialize new project")
        sys.exit(1)

    args = sys.argv[1:]

    if "--init" in args:
        if not os.listdir("."):
            initiating()
        else:
            print_panic("Cannot initialize: current folder is not empty.")
            print_info("Please use 'cherry --init' in an empty directory.")
        return

    # .cb 파일 추출
    cb_path = next((arg for arg in args if arg.endswith(".cb")), None)

    if not cb_path:
        print_panic("No .cb file specified.")
        return

    if "--tocpp" in args:
        compile_cb(cb_path, istoexe=False)
    else:
        compile_cb(cb_path, istoexe=True)


if __name__ == "__main__":
    main()
