#!/usr/bin/python3
import sys

inf = 10**100


class LangData(object):
    """Docstring for LangData. """

    def __init__(self, prefix_set, ans, min_word):
        """Init LangData

        :prefix_set: possible prefix set
        :ans: answer for language. if exists. Otherwise, INF
        :min_word: minimal word in language

        """
        self.prefix_set = prefix_set
        self.ans = ans
        self.min_word = min_word

    def __str__(self):
        return str(self.prefix_set) + ' ' + str(self.ans) + ' ' + str(
            self.min_word)


def concat_langs(fst, snd, mlen):
    np = LangData(set(), inf, inf)
    np.min_word = fst.min_word + snd.min_word
    np.ans = fst.ans + snd.min_word
    for s1 in fst.prefix_set:
        np.prefix_set.add((s1[0], s1[1] + snd.min_word))
        if s1[0] != s1[1]:
            continue
        for s2 in snd.prefix_set:
            nvar = s1[0] + s2[0]
            np.prefix_set.add((nvar, s1[1] + s2[1]))
            if nvar >= mlen:
                np.ans = min(np.ans, s1[1] + s2[1])
    return np


def unite_langs(fst, snd):
    np = LangData(set(), inf, inf)
    np.min_word = min(fst.min_word, snd.min_word)
    np.ans = min(fst.ans, snd.ans)
    np.prefix_set = fst.prefix_set | snd.prefix_set
    return np


def asteriks_lang(cur, mlen):
    np = LangData(set(), inf, inf)
    np.min_word = 0
    np.prefix_set.add((0, 0))
    cur_power = cur
    for i in range(mlen):
        ncur_power = concat_langs(cur_power, cur, mlen)
        np = unite_langs(np, cur_power)
        cur_power = ncur_power
    return np


def find_minimal(regular_string, myx, mlen):
    try:
        reg_stack = list()
        lang_stack = list()
        for symbol in regular_string:
            if symbol == ' ':
                continue
            elif symbol == '.':
                snd, fst = lang_stack.pop(), lang_stack.pop()
                lang_stack.append(concat_langs(fst, snd, mlen))
            elif symbol == '+':
                snd, fst = lang_stack.pop(), lang_stack.pop()
                lang_stack.append(unite_langs(fst, snd))
            elif symbol == '*':
                lang_stack.append(asteriks_lang(lang_stack.pop(), mlen))
            elif symbol == '1':
                lang_stack.append(LangData(set(), inf, 0))
                lang_stack[-1].prefix_set.add((0, 0))
            else:
                reg_stack.append(symbol)
                if symbol != 'a' and symbol != 'b' and symbol != 'c':
                    print("ERROR")
                    sys.exit(0)
                lang_stack.append(LangData(set(), inf, 1))
                if symbol == myx:
                    lang_stack[-1].prefix_set.add((1, 1))
                    if mlen == 1:
                        lang_stack[-1].ans = 1
    except IndexError:
        print('ERROR')
        sys.exit(0)
    if len(lang_stack) != 1:
        print('ERROR')
        sys.exit(0)
    if lang_stack[0].ans >= inf:
        return 'INF'
    return lang_stack[0].ans


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


if __name__ == '__main__':
    main()
