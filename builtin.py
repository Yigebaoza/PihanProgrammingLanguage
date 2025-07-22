import sys

ERROR = (NameError, SyntaxError)


class Sys:
    def __init__(self):
        self.so = sys.stdout
        self.si = sys.stdin
        self.io = sys.stdin, sys.stdout

def write(x, pos):
    """
    :param x:
    :param pos:
    :return None:
    实现一个write函数，用于向指定位置写入内容
    """
    if pos is sys.stdout or pos is sys.stdin:
        try:
            y = eval(x)
            print(y, end='')
        except ERROR:
            print(x, end='')
    else:
        with open(pos, 'w') as f:
            try:
                y = eval(x)
            except ERROR:
                y = x
            f.write(y)

def writeln(x, pos):
    """
    :param x:
    :param pos:
    :return None:
    实现一个writeln函数，用于向指定位置写入内容并换行
    """
    if pos is sys.stdout or pos is sys.stdin:
        try:
            y = eval(x)
            print(y)
        except ERROR:
            print(x)
    else:
        with open(pos, 'w') as f:
            try:
                y = eval(x)
            except ERROR:
                y = x
            f.write(y+"\n")

def append(x, pos):
    """
    :param x:
    :param pos:
    :return None:
    实现一个append函数，用于向指定位置添加内容
    """
    if pos is sys.stdout or pos is sys.stdin:
        try:
            y = eval(x)
            print(y, end='')
        except ERROR:
            print(x, end='')
    with open(pos, 'a') as f:
        try:
            y = eval(x)
        except ERROR:
            y = x
        f.write(y)
        
def appendln(x, pos):
    """
    :param x:
    :param pos:
    :return None:
    实现一个append函数，用于向指定位置添加内容
    """
    if pos is sys.stdout or pos is sys.stdin:
        try:
            y = eval(x)
            print(y)
        except ERROR:
            print(x)
    with open(pos, 'a') as f:
        try:
            y = eval(x)
        except ERROR:
            y = x
        f.write(y+"\n")

def readchar(pos):
    """
    :param pos:
    :return None:
    """
    if pos is sys.stdout or pos is sys.stdin:
        return ""
    return pos.read(1)

def readln(pos):
    """
    :param pos:
    :return None:
    """
    if pos is sys.stdout or pos is sys.stdin:
        return ""
    return pos.readline()

def read(pos, length=-1):
    """
    :param pos:
    :param length:
    :return:
    """
    if pos is sys.stdout or pos is sys.stdin:
        return ""
    if length == -1:
        return pos.read()
    return pos.read(length)

def ward(x, pos, length=-1):
    """
    :param x:
    :param pos:
    :param length:
    :return:
    """
    if length == 0 or (pos == sys.stdout or pos == sys.stdin):
        try:
            y = eval(x)
        except ERROR:
            y = x
        return input(y)

    write(x, pos[0])
    return read(pos[1], length)


system = Sys()
PHAN_BUILTINS = {
    'sys': system,
    'so': system.so,
    'si': system.si,
    'io': system.io,
    'wardln': lambda text, pos, length=0: ward(text, pos, length),
    'ward': lambda text, pos, length=0: ward(text, pos, length),
    'writeln': lambda text, stream: writeln(text, stream),
    'write': lambda text, stream: write(text, stream),
    'append': lambda text, stream: append(text, stream),
    'appendln': lambda text, stream: appendln(text, stream),
    'readchar': lambda pos: readchar(pos),
    'readln': lambda pos: readln(pos),
    'read': lambda pos, length=0: read(pos, length)
}
