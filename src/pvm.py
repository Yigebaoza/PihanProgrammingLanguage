"""
load: 申请一块内存空间(self.space["name"] = None)
setv: 设置内存中的名称(self.space["name"] = value)
show: 显示内存中的名称对应的值
type: 发起输入操作
delv: 删除内存中的名称
xxx: 将两个名称对应的值相x存到xtmp
comp: 比较两个名称的值
true: 为真时执行
fals: 为假时执行

示例：
load a 0
load b 0
load c 0
setv a "HelloWorld"
setv b "HelloWorld"
show a 0
type a "HelloWorld"
comp a b
true ctmp 1:
    show a 0
fals ctmp 0:
    show b 0
add a b
setv c atmp

delv a 0
delv b 0
delv c 0

bin:
0000000...00000000000000000000000000000000000000000000000000000000000000000000000000000000
0001000...01001000011001010110110001101100011011110101011101101111011100100110110001100100
0002000...00000000000000000000000000000000000000000000000000000000000000000000000000000000
0004000...00000000000000000000000000000000000000000000000000000000000000000000000000000000
.....
"""

ISA = {
    b"\x00": "load",
    b"\x01": "setv",
    b"\x02": "show",
    b"\x03": "type",
    b"\x04": "delv",
    b"\x05": "addn",
    b'\x06': "subn",
    b'\x07': "muln",
    b'\x08': "divn",
    b'\x09': "comn",
    b'\x0A': "true",
    b'\x0B': "fals",
}


class PihanVirtualMachine:
    def __init__(self):
        self.space = {}

    def exec_file(self, file):
        lines = file.readlines()
        self._exec_lines(lines)

    def _exec_lines(self, lines: list[bytes]) -> None:
        for line in lines:
            line = line.strip()
            if line.startswith(b"\t"):
                continue
            oper, a, b = line.split(b" ", 2)
            match ISA[oper]:
                case "load":
                    self.space[a] = None
                case "setv":
                    self.space[a] = b
                case "show":
                    if b == b"\x00":
                        if self.space.get(a, True):
                            print(a.decode())
                        else:
                            print(self.space[a].decode())
                    elif b == b"\x01":
                        if self.space.get(a, True):
                            print(a.decode(), end="")
                        else:
                            print(self.space[a].decode(), end="")
                case "type":
                    self.space[a] = input(b)
                case "delv":
                    del self.space[a]
                case "addn":
                    self.space["atmp"] = eval(f"{a}+{b}", self.space)
                case "subn":
                    self.space["stmp"] = eval(f"{a}-{b}", self.space)
                case "muln":
                    self.space["mtmp"] = eval(f"{a}*{b}", self.space)
                case "divn":
                    self.space["dtmp"] = eval(f"{a}/{b}", self.space)
                case "comn":
                    self.space["ctmp"] = eval(f"{a}=={b}", self.space)
                case "true":
                    self._exec_true_stat(a, lines.index(line), lines)
                case "fals":
                    self._exec_fals_stat(a, lines.index(line), lines)

    def _exec_true_stat(self, a, cur_line_index, lines):
        if not eval(a, self.space):
            return
        stop = 0
        for line in lines[cur_line_index:]:
            if not line.startswith("\t"):
                stop = lines.index(line) - 1
        self._exec_lines([i for i in lines[cur_line_index:stop]])

    def _exec_fals_stat(self, a, cur_line_index, lines):
        if eval(a, self.space):
            return
        stop = 0
        for line in lines[cur_line_index:]:
            if not line.startswith("\t"):
                stop = lines.index(line) - 1
        self._exec_lines([i for i in lines[cur_line_index:stop]])
