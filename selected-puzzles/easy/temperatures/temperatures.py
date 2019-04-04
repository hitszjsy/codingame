# the number of temperatures to analyse
n = int(input())
min_t = 5526
for i in input().split():
    # t: a temperature expressed as an integer ranging from -273 to 5526
    t = int(i)
    if abs(t) < abs(min_t) or abs(t) == abs(min_t) and t > min_t:
        min_t = t

print(0 if n == 0 else min_t)
