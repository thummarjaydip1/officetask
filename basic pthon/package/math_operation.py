def add(*args):
    if len(args) <=1:
        return "plase enter minimum 2 argument"

    total = 0
    for i in args:
        total += i

    return total

def mul(*args):
    if len(args) <=1:
        return "plase enter minimum 2 argument"

    total = 1
    for i in args:
        total *= i

    return total
