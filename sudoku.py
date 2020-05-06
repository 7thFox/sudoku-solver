import numpy as np

backtrack = 0


def check_full(p, solution):
    return all(np.array(p) == np.array(solution))


def col(p, i):
    return np.array(p[i::9])


def row(p, i):
    return np.array(p[i * 9:i * 9 + 9])


def section(p, i):
    s = i % 3 * 3 + i // 3 * 27
    return np.array(p[s + 0*0:s + 0*9 + 3] +
                    p[s + 1*9:s + 1*9 + 3] +
                    p[s + 2 * 9:s + 2 * 9 + 3])


def check(p):
    def _check(ck):
        if any(ck == 0):
            return len(np.unique(ck)) - np.count_nonzero(ck) == 1
        else:
            return len(np.unique(ck)) == 9

    for i in range(0, 9):
        if not (_check(col(p, i)) and
                _check(row(p, i)) and
                _check(section(p, i))):
            return False

    return True


def imply(p):
    changed = False
    p = p.copy()

    for i in range(0, 81):
        if p[i] != 0:
            continue
        a = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        row_n = i // 9
        col_n = i % 9
        section_n = (row_n // 3) * 3 + col_n // 3

        prob = a.difference(row(p, row_n)) \
            .difference(col(p, col_n)) \
            .difference(section(p, section_n))
        if len(prob) == 1:
            changed = True
            p[i] = next(iter(prob))

    if changed:
        return imply(p)
    return p


def _solve(p, loc):
    global backtrack
    if not check(p):
        return None
    if loc >= 81:
        return p
    if p[loc] != 0:
        return _solve(p, loc+1)

    p_i = p.copy()
    for i in range(1, 10):
        p_i[loc] = i
        sub_p = _solve(imply(p_i), loc+1)
        if sub_p is not None:
            return sub_p
        backtrack += 1
    return None


def solve(puzzle, solution):
    global backtrack

    backtrack = 0
    puzzle = imply([int(x) for x in puzzle])
    solution = [int(x) for x in solution]

    sol = _solve(puzzle, 0)
    if check_full(sol, solution):
        return backtrack
    return None


# "Worlds Hardest" sudoku: https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html
puzzle = imply(
    [int(x) for x in "800000000003600000070090200050007000000045700000100030001000068008500010090000400"])
print(np.reshape(_solve(puzzle, 0), (9, 9)))
print(backtrack)

# Reads in csv of puzzle/solution pairs from kaggle: https://www.kaggle.com/bryanpark/sudoku/discussion

# i = 0
# with open("sudoku.csv") as csv:
#     csv.readline()  # Headers
#     t = 0
#     mn = 99999
#     mx = -1
#     while True:  # and i < 500:
#         print("\r"+str(i), end="")
#         i += 1
#         if i < 5000:
#             continue
#         line = csv.readline()
#         if not line:
#             break
#         p_s = line.split(',')
#         s = solve(p_s[0].strip(), p_s[1].strip())
#         t += s
#         mn = min(mn, s)
#         mx = max(mx, s)
#         if i % 250 == 0:
#             print("\nMean: ", t / i)
#             print("Min: ", mn)
#             print("Max: ", mx)
