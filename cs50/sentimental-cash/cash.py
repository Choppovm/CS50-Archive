from cs50 import get_float

c1 = 0
main = 0
while c1 <= 0:
    c1 = get_float("Change owed: ")
    c2 = round(c1 * 100)
while c2 > 0:
    if c2 >= 25:
        c2 = c2 - 25
        main = main + 1
    elif c2 >= 10:
        c2 = c2 - 10
        main = main + 1
    elif c2 >= 5:
        c2 = c2 - 5
        main = main + 1
    elif c2 >= 1:
        c2 = c2 - 1
        main = main + 1
print(main)
