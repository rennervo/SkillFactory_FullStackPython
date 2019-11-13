count = 0
for i in range(1, 10000):
    if i % 3 == 0:
        count += i
    elif i % 5 == 0:
        count += i
    elif i % 7 == 0:
        count += i
print(count)
