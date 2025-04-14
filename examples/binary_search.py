
from typing import TypeVar, Optional, Protocol

from tracelist import tracelist
from rich import print


class Comparable(Protocol):
    def __lt__(self, other) -> bool:
        pass
        

A = TypeVar("A", bound=Comparable)


def binary_search(src: list[A], value: A) -> int:
    low: int = 0
    high: int = len(src) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if src[mid] == value:
            return mid
        if value < src[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1

    
data = tracelist([10, 11, 13, 15, 18, 28, 29, 30, 41, 41, 45, 46, 47, 51, 64, 74, 82, 82, 83, 92, 97])
data.sort()
print(data)
print(binary_search(data, 29))
print(data)

