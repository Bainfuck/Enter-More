#coding=utf-8
import sys
import string

栈: list = []
寄存带: list = [0]
纸带指针: int = 0

def enter_more_translator(指令流: str):
    指令流原子集: list = []
    while 指令流:
        if 指令流.startswith(">>"):
            指令流原子集.append(">>")
            指令流 = 指令流[2:]
        elif 指令流.startswith("<<"):
            指令流原子集.append("<<")
            指令流 = 指令流[2:]
        elif 指令流.startswith("?~!"):
            指令流原子集.append("?~!")
            指令流 = 指令流[3:]
        elif 指令流.startswith("!~?"):
            指令流原子集.append("!~?")
            指令流 = 指令流[3:]
        elif 指令流.startswith("?~"):
            指令流原子集.append("?~")
            指令流 = 指令流[2:]
        elif 指令流.startswith("!~"):
            指令流原子集.append("!~")
            指令流 = 指令流[2:]
        elif 指令流.startswith("?!"):
            指令流原子集.append("?!")
            指令流 = 指令流[2:]
        elif 指令流.startswith("!?"):
            指令流原子集.append("!?")
            指令流 = 指令流[2:]
        elif 指令流[0] in "+-)?!><Xx":
            指令流原子集.append(指令流[0])
            指令流 = 指令流[1:]
        elif 指令流[0] in string.hexdigits:
            pos = 0
            while pos < len(指令流) and 指令流[pos] in string.hexdigits:
                pos += 1
            num_str = 指令流[:pos]
            if pos < len(指令流) and 指令流[pos] == '(':
                指令流原子集.append(['(', int(num_str, 16)])
                pos += 1
            else:
                指令流原子集.append(int(num_str, 16))
            指令流 = 指令流[pos:]
        elif 指令流.startswith("\n"):
            pos = 0
            while pos < len(指令流) and 指令流[pos] == "\n":
                pos += 1
            指令流原子集.append({pos})
            指令流 = 指令流[pos:]
        elif 指令流.startswith(" "):
            pos = 0
            while pos < len(指令流) and 指令流[pos] == " ":
                pos += 1
            指令流原子集.append({-pos})
            指令流 = 指令流[pos:]
        elif 指令流.startswith("("):
            指令流.append("(")
        else:
            指令流 = 指令流[1:]
    return 指令流原子集

def complier(指令流: list):
    global 栈, 纸带指针, 寄存带
    指令指针: int = 0
    指令流长 = len(指令流)
    while 指令指针 < 指令流长:
        原子 = 指令流[指令指针]

        if 原子 == ">":
            纸带指针 += 1
            if len(寄存带) == 纸带指针:
                寄存带.append(0)
            elif 纸带指针 == 1:
                if 寄存带[0] == 0:
                    纸带指针 = 0
                    寄存带.pop(0)
        elif 原子 == "<":
            纸带指针 -= 1
            if len(寄存带) - 2 == 纸带指针:
                if 寄存带[-1] == 0:
                    寄存带.pop()
            elif 纸带指针 == -1:
                纸带指针 = 0
                寄存带.insert(0, 0)
        elif 原子 == "+":
            寄存带[纸带指针] += 1
        elif 原子 == "-":
            寄存带[纸带指针] -= 1
        elif 原子 == "?":
            栈.append(寄存带[纸带指针])
        elif 原子 in "Xx":
            for i in reversed(input()):
                栈.append(ord(i))
        elif 原子 == "?!":
            print(寄存带[纸带指针])
        elif 原子 == "!?":
            try:
                print(chr(栈.pop()), end="")
            except ValueError:
                print("栈顶有非法文本！")
                break
            except IndexError:
                print(chr(0), end="")
        elif 原子 == "!~":
            if 纸带指针 == 0 and len(寄存带) > 1:
                寄存带[纸带指针 + 1] = 0
            elif 纸带指针 == len(寄存带) - 1:
                寄存带[纸带指针 - 1] = 0
            else:
                寄存带[纸带指针 - 1], 寄存带[纸带指针 + 1] = 寄存带[纸带指针 + 1], 寄存带[纸带指针 - 1]
        elif 原子 == "?~":
            if len(栈) > 1:
                栈[-1], 栈[-2] = 栈[-2], 栈[-1]
            elif len(栈) == 1:
                栈[-1] = 0
        elif 原子 == ">>":
            try:
                栈.pop()
            except IndexError:
                pass
        elif 原子 == "<<":
            if 指令指针 + 1 < 指令流长 and type(指令流[指令指针 + 1]) == int:
                栈.append(指令流[指令指针 + 1])
                指令指针 += 1
            else:
                栈.append(0)
        elif 原子 == "?~!":
            栈.append(~(栈[-1] & 寄存带[纸带指针]))
        elif 原子 == "!~?":
            寄存带[纸带指针] = ~(栈[-1] & 寄存带[纸带指针])
        elif 原子 == ")":
            if 寄存带[纸带指针] != 0:
                回溯指针 = 指令指针 - 1
                while 回溯指针 >= 0:
                    if 指令流[回溯指针] == "(" and type(指令流[回溯指针]) != list:
                        break
                    回溯指针 -= 1
                指令指针 = 回溯指针 + 1  # 没找到时变成 0
            continue
        elif type(原子) == set:
            指令指针 += tuple(原子)[0] % 指令流长
        elif 原子 == "(":
            if 寄存带[纸带指针] == 0:
                前进指针 = 指令指针 + 1
                while 前进指针 < 指令流长 and 指令流[前进指针] != ")":
                    前进指针 += 1
                指令指针 = 前进指针  # 没找到时变成 指令流长
            continue
        else:  # 循环指令 ['(', 次数]
            roundtime = 原子[1]
            循环起点 = 指令指针 + 1
            循环终点 = 循环起点
            while 循环终点 < 指令流长 and 指令流[循环终点] != ")":
                循环终点 += 1
            # 找不到 ) 时，循环终点 = 指令流长（与指令流尾构成循环）
            for _ in range(roundtime):
                complier(指令流[循环起点:循环终点])
            指令指针 = 循环终点
            continue

        指令指针 += 1

if len(sys.argv) > 1:
    try:
        with open(sys.argv[1]) as emfile:
            emfile = emfile.read().split("\t")
            codeflow = []
            for i in emfile:
                codeflow.extend(enter_more_translator(i))
            complier(codeflow)
    except FileNotFoundError:
        print("我没找到文件……")
