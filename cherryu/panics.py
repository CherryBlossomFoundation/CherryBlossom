import sys

from .status import print_panic

def get_caller_filename():
    stack = traceback.extract_stack()
    for frame in reversed(stack):
        if not frame.filename.endswith("panics.py"):
            return os.path.abspath(frame.filename)
    return None

class Panic:
    def __init__(self, msg, line=None, code=1, key=None, filename=None):
        self.key = key
        self.msg = msg
        self.line = line
        self.filename = filename or get_caller_filename()
        self.code = code
        self.trigger()

    def trigger(self):
        print_panic(f"Panic! [{self.__class__.__name__}]")

        if self.filename:
            print_panic(f"file: {self.filename}")

        if self.line is not None:
            print_panic(f"line: {self.line}")
            if self.key is not None:
                print_panic(f"{self.line} -> {self.key}")
                print_panic(f"{self.msg}")
            else:
                print_panic(f"{self.msg}")
        else:
            print_panic(self.msg)



        sys.exit(self.code)


class PanicSyntaxError(Panic):
    def __init__(self, msg, key, line=None, filename=None):
        super().__init__(msg, line, key=key, code=-101, filename=filename)


class PanicKeywordError(Panic):
    def __init__(self, msg, key, line=None, filename=None):
        super().__init__(msg, line, key=key, code=-102, filename=filename)


class PanicCompileError(Panic):
    def __init__(self, msg, line=None, filename=None):
        super().__init__(msg, line, code=-1, filename=filename)


class PanicNotDefinedError(Panic):
    def __init__(self, msg, key, line=None, filename=None):
        super().__init__(msg, line, key=key, code=-202, filename=filename)