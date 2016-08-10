a = [3,5,7,2,5,3,6]
for j in range(1, len(a)):
    key = a[j]
    i = j -1
    while i >= 0 and a[i] > key:
        a[i+1] = a[i]
        i -= 1
    a[i+1] = key
print(a)
