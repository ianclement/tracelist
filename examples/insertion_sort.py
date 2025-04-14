# this isn't recursion just a test of the trace list

from typing import TypeVar, Optional, Protocol

from tracelist import tracelist
from rich import print


class Comparable(Protocol):
    def __lt__(self, other) -> bool:
        pass
        

A = TypeVar("A", bound=Comparable)


def insertion_sort(data: list[A]):
    for i in range(len(data)):
        print(f"Placing data[{i}]")
        j: int = i
        while j > 0 and data[j - 1] > data[j]:
            data[j - 1], data[j] = data[j], data[j - 1]
            j -= 1

        print(data)

    
data = tracelist("asdfzkljaflkzjasflkzsad")

#data.read_color(lambda rc, _1, _2: f"on rgb(0,{min(255,rc*4+40)},{min(255,rc*4+40)})")
#data.write_color(lambda _1, _2, c: c)
data.read_color("green")
data.write_color("red")
insertion_sort(data)
print(data)


