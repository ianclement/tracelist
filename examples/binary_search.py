
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

    
data = tracelist("asdfzkljaflkzjasflkzsad")
data.sort()
print(data)
print(binary_search(data, "f"))
print(data)

