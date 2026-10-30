from itertools import combinations

def can_make_lucky_ticket(digits: tuple) -> bool:
    s = sum(digits)
    return s % 2 == 0 and any(sum(d) == s // 2 for d in combinations(digits, 3))
