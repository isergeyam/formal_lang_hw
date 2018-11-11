#!/usr/bin/python3
import sys

inf = 10**100


class LangData(object):
    """Docstring for LangData. """

    def __init__(self, prefix_set, ans, min_word):
        # if pos_prefix == None:
        #     pos_prefix = set()
        """Init LangData

        :prefix_set: possible prefix set
        :ans: answer for language. if exists. Otherwise, INF
        :min_word: minimal word in language

        """
        self._prefix_set = prefix_set
        self._ans = ans
        self._min_word = min_word
        # self._pos_prefix = pos_prefix
    def __str__(self):
        return str(self._prefix_set) + ' ' + str(self._ans) + ' ' + str(
            self._min_word)


def find_minimal(regular_string, myx, mlen):
    try:
        reg_stack = list()
        lang_stack = list()
        for symbol in regular_string:
            if symbol == ' ':
                continue
            elif symbol == '.':
                np = LangData(set(), inf, inf)
                snd, fst = lang_stack.pop(), lang_stack.pop()
                np._min_word = fst._min_word + snd._min_word
                np._ans = fst._ans + snd._min_word
                for s1 in fst._prefix_set:
                    np._prefix_set.add((s1[0], s1[1] + snd._min_word))
                    if s1[0] != s1[1]:
                        continue
                    for s2 in snd._prefix_set:
                        nvar = s1[0] + s2[0]
                        np._prefix_set.add((nvar, s1[1] + s2[1]))
                        if nvar >= mlen:
                            np._ans = min(np._ans, s1[1] + s2[1])
                lang_stack.append(np)
            elif symbol == '+':
                np = LangData(set(), inf, inf)
                snd, fst = lang_stack.pop(), lang_stack.pop()
                np._min_word = min(fst._min_word, snd._min_word)
                np._ans = min(fst._ans, snd._ans)
                np._prefix_set = fst._prefix_set | snd._prefix_set
                lang_stack.append(np)
            elif symbol == '*':
                np = LangData(set(), inf, inf)
                cur = lang_stack.pop()
                np._ans = cur._ans
                np._min_word = 0
                np._prefix_set.add((0, 0))
                for s in cur._prefix_set:
                    if s[0] != s[1] or s[0] == 0:
                        np._prefix_set.add(s)
                        continue
                    ns = s[0]
                    while ns - s[0] < mlen:
                        np._prefix_set.add((ns, ns))
                        if ns >= mlen:
                            np._ans = min(np._ans, ns)
                        ns += s[0]
                lang_stack.append(np)
            elif symbol == '1':
                lang_stack.append(LangData(set(), inf, 0))
                lang_stack[-1]._prefix_set.add((0, 0))
            else:
                reg_stack.append(symbol)
                if symbol != 'a' and symbol != 'b' and symbol != 'c':
                    print("ERROR")
                    sys.exit(0)
                lang_stack.append(LangData(set(), inf, 1))
                if symbol == myx:
                    lang_stack[-1]._prefix_set.add((1, 1))
                    if mlen == 1:
                        lang_stack[-1]._ans = 1
    except IndexError:
        print('ERROR')
        sys.exit(0)
    if len(lang_stack) != 1:
        print('ERROR')
        sys.exit(0)
    if lang_stack[0]._ans >= inf:
        return 'INF'
    return lang_stack[0]._ans


def get_reg_str(reg):
    reg_stack = list()
    for symb in reg:
        if symb == '.' or symb == '+':
            snd, fst = reg_stack.pop(), reg_stack.pop()
            reg_stack.append('(' + fst + symb + snd + ')')
        elif symb == '*':
            reg_stack.append('(' + reg_stack.pop() + ')*')
        else:
            reg_stack.append(symb)
    return reg_stack[0]


def main():
    print(find_minimal(input(), input(), int(input())))
    #print(get_reg_str(input()))


if __name__ == '__main__':
    main()
