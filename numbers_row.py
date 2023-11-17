n = int(input())
string = ''
for num in range(1, n + 1):
    string += str(num) * num
    if len(string) >= n:
        break
print(string[:n])
