current, tmp1, tmp2 = 0, 1, 2
even = 2
while current < 4000000:
    current = tmp1 + tmp2
    tmp1, tmp2 = tmp2, current
    print(current)
    if current % 2 == 0:
        even += current
print("Cумма четных чисел = {}".format(even))
