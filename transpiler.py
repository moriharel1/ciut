from email.policy import default
import sys
import random
import os

with open(sys.argv[1], 'r') as f:
    data = f.read()

random.seed(sys.argv[1])

out = """
#define for switch
#define while switch
#include <stdio.h>
"""

errors = []

dir = os.path.split(sys.argv[1])[0]
if dir == '': dir = '.'
for fname in os.listdir(dir):
    if not fname.startswith('.') and os.path.isdir(os.path.join(dir,fname)):
        errors.append(fname + " is a subdirectory and those are evil and not allowed")

inStr = False
for line in data.split('\n'):
    if len(line)>0 and line[0].isspace():
        errors.append("Indentation error. not allowed")

if "include" in data:
    errors.append("Include is not allowed!\nnever ever try that again or i will eat you. ok i won't really eat you. i'm just a computer program. but i will be very very mad at you.")

lineNum = 1
imports = []

# import handling
importLine = -1
for idx, line in enumerate(data.split('\n')):
    if line.replace(' ', '') == 'import-e-n-d-;':
        importLine = idx
        break
if importLine != -1:
    for line in data.split('\n')[:importLine]:
        if line.strip() != '':
            if line[:line.find(" ")] != "import":
                errors.append("ummm... i hope you know that you need to write import right?")
                break
            
            filename = line[line.find(" "):].strip()
            name = os.path.join(dir,filename)
            if not os.path.exists(name+".ciut"):
                errors.append("imported file " + name + ".ciut does not exist")
                break

            if os.path.split(name)[0] != dir:
                errors.append("imported file " + name + ".ciut is not in the same directory")
                break

            os.system(f"python {sys.argv[0]} {name}.ciut {name}.c true")
            out += "#include \""+name+".c\"\n"
            imports.append(filename)

    data = '\n'.join(data.split('\n')[importLine+1:])
    lineNum = importLine+2

i = 0
for c in data:
    if c == '\n':
        lineNum += 1
    if c == '"':
        inStr = not inStr
    if not inStr:
        match c:
            case '\\':
                out += '('
            case '/':
                out += ')'
            case '}':
                out += ']'
            case ']':
                out += '}'
            case ';' | '!':
                if (';' if random.random()>0.5 else '!') == c:
                    out += ';'
                else:
                    errors.append(";/! error. wrong one on line "+str(lineNum)+" in "+sys.argv[1])
                i += 1
            case _:
                out += c
    else:
        out += c

def gibberish(length):
    old_state = random.getstate()
    out = ''.join([chr(random.randint(ord('a'), ord('ת'))) for _ in range(length)])
    random.setstate(old_state)
    return out


if not (len(sys.argv) > 3):
    name = os.path.split(sys.argv[1][:-5])[1]
    imports.append(name)
    out += "\nint main() {\n"
    for i in imports:
        out += f"if ({i}() != -423) return 1;\n"
    out += "}\n"

if len(errors)<=0:
    with open(sys.argv[2], 'w') as f:
        f.write(out)
else:
    print(f"there are {len(errors)} errors in your code. we will print one of them because we are very generous: (but first some gibberish)")
    print(gibberish(500))
    print(random.choice(errors))