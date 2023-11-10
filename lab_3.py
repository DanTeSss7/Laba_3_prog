equations = """\
17*4+(x*54/(2+4))=y
2+2
18*41*с
+45
17+4*
(34+1,45*3)
(4+5)) 
"""

import re

REGEX = re.compile(r"(([a-zA-Z]|\d+)[\+\-\/\*]){1,}([a-zA-Z]|\d+)(=([a-zA-Z]|\d+))?")
def matches(line, opendelim='(', closedelim=')'):
    stack = []
    for m in re.finditer(r'[{}{}]'.format(opendelim, closedelim), line):
        pos = m.start()
        if line[pos - 1] == '\\':
            continue
        c = line[pos]
        if c == opendelim:
            stack.append(pos + 1)
        elif c == closedelim:
            if len(stack) > 0:
                prevpos = stack.pop()
                yield (True, prevpos, pos, len(stack))
            else:
                yield (False, 0, 0, 0)
                pass
    if len(stack) > 0:
        for pos in stack:
            yield (False, 0, 0, 0)


def isPartCorrect(s):
    result = False
    if REGEX.match(s) and s[-1] not in "+-*/":
        result = True
    return result


def isCorrect(s):
    result = True
    if s.find("(") >= 0 or s.find(")") >= 0:
        for correct, openpos, closepos, level in matches(s):
            if correct:
                part = s[openpos:closepos]
                if part.find("(") == -1 and part.find(")") == -1:
                    if not isPartCorrect(part):
                        result = False
                        break
                part = s[openpos - 1:closepos + 1]
                replaced = s.replace(part, "p")
                if replaced.find("(") >= 0 or replaced.find(")") >= 0:
                    if not isCorrect(replaced):
                        result = False
                        break
                else:
                    if not isPartCorrect(replaced):
                        result = False
                        break
            else:
                result = False
                break
    else:
        result = isPartCorrect(s)
    return result

print(isCorrect("18*"))