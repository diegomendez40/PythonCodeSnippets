# Read input from STDIN.
[n, m] = list(map(int, input().split()))

# Check valid size
if n % 2 == 0 or m % 3 != 0:
    raise ValueError("n must be odd, m must be a multiple of 3\nn debe ser impar y m debe ser múltiplo de 3")

c = n // 2

# Upper pattern
for i in range(c):
    times = (m - 3 * (1 + 2 * i)) // 2
    line = "-" * times + ".|." * (1 + 2 * i) + "-" * times
    print(line)

# Central pattern
line = "-" * (( m - 7) // 2) + 'WELCOME' + "-" * ((m - 7) // 2) 
print(line)
line = "-" * (( m - 15) // 2) + "diegomendez40's" + "-" * ((m - 15) // 2)
print(line)
line = "-" * (( m - 9) // 2) + "PYTHONICS" + "-" * ((m - 9) // 2)
print(line)

# Lower pattern
for i in range(c):
    times = (m - 3 *(1 + 2 *(c - 1 - i))) // 2 
    line = "-" * times + ".|." * (1 + 2 * (c-i-1)) + "-" * times
    print(line)