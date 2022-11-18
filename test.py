import math
import sys

p = ""
with open('pServer.txt', 'r') as file:
    p = int(file.read().rstrip())


print(p**2)
print(sys.maxsize)
divide = p**2 / sys.maxsize
print(math.floor(divide))
modulo = p**2 % sys.maxsize
print(modulo)
print(sys.maxsize > modulo) 
print(sys.maxsize > divide)
print(p**2 == (sys.maxsize * math.floor(divide) + modulo))