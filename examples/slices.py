from tracelist import tracelist

from rich import print


data = tracelist([26, 81, 44, 99, 67, 79, 90])

print("Read data[2:6]")
print(data[2:6])
print()
print(data)

print("Write data[2:6] = [32, 12]")
data[2:6] = [32, 12]
print(data)

