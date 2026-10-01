"""Minimal S-expression parser for KiCad files (netlist, sch, pcb)."""
import re, sys

TOKEN = re.compile(r'\s*(?:(\()|(\))|("(?:[^"\\]|\\.)*")|([^\s()"]+))', re.S)


def parse(text):
    stack = [[]]
    pos = 0
    n = len(text)
    while pos < n:
        m = TOKEN.match(text, pos)
        if not m:
            if text[pos:].strip() == "":
                break
            raise ValueError("parse error at %d: %r" % (pos, text[pos:pos + 50]))
        pos = m.end()
        if m.group(1):
            stack.append([])
        elif m.group(2):
            top = stack.pop()
            stack[-1].append(top)
        elif m.group(3) is not None:
            s = m.group(3)[1:-1]
            s = s.replace('\\"', '"').replace('\\\\', '\\')
            stack[-1].append(Str(s))
        elif m.group(4) is not None:
            stack[-1].append(m.group(4))
    return stack[0][0] if len(stack[0]) == 1 else stack[0]


class Str(str):
    """Quoted string marker."""
    pass


def find(node, name):
    """Direct children lists whose head == name."""
    return [c for c in node if isinstance(c, list) and c and c[0] == name]


def find1(node, name, default=None):
    r = find(node, name)
    return r[0] if r else default


def walk(node, name):
    """All descendants (recursive) whose head == name."""
    out = []
    if isinstance(node, list):
        if node and node[0] == name:
            out.append(node)
        for c in node:
            if isinstance(c, list):
                out.extend(walk(c, name))
    return out


def val(node, name, default=None):
    r = find1(node, name)
    if r is None or len(r) < 2:
        return default
    return r[1]


def load(path):
    with open(path, encoding="utf-8") as f:
        return parse(f.read())
