print("For the square pattern")
s = 5
for i in range(s):
    for j in range(s):
        print('*', end=' ')
    print()

print("For the triangle patterns")
n = 5
for i in range(n):
    for j in range(n-i-1):
        print(end=' ')
    for j in range(i*2+1):
        print('*', end='')
    print()

print("For the pyramid")
n = 5
for i in range(n):
    for j in range(n-i-1):
        print(end=' ')
    for j in range(i*2+1):
        print('*', end='')
    print()

def draw_diamond(n):
    for i in range(1, n + 1):
        print(" " * (n - i) + "* " * i)
    for i in range(n - 1, 0, -1):
        print(" " * (n - i) + "* " * i)

# Example usage
draw_diamond(5)
