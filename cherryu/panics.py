import sys

from .status import print_panic

class Panic:

    def __init__(self,  msg, line=None, code=1, key=None):
        self.key = key
        self.msg = msg
        self.line = line
        self.code = code
        self.trigger()

    def trigger(self):
        print_panic(f"Panic! [{self.__class__.__name__}]")
        if self.line is not None:
            if self.key is not None:
                print_panic(f"at: line {self.line}")
                print_panic(f"{self.line} -> {self.key}")
                print_panic(f"{self.msg}")
            else:
                print_panic(f"at: line {self.line}")
                print_panic(f"{self.msg}")
        else:
            print_panic(self.msg)
        sys.exit(self.code)

class PanicSyntaxError(Panic):
    def __init__(self, msg, key, line=None):
        super().__init__(msg, line, key=key ,code=-101)


class PanicKeywordError(Panic):
    def __init__(self, msg, key,line=None):
        super().__init__(msg, line, key=key, code=-102)


class PanicCompileError(Panic):
    def __init__(self, msg, line=None):
        super().__init__(msg, line, code=-1)

class PanicNotDefinedError(Panic):
    def __init__(self, msg, key, line=None):
        super().__init__(msg, line, key=key, code=-202)