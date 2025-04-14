# this isn't recursion just a test of the trace list

from typing import TypeVar, Optional, Protocol

from trace_list import tracelist
from rich.console import Console

console: Console = Console()

class Comparable(Protocol):
    def __lt__(self, other) -> bool:
        pass
        

A = TypeVar("A", bound=Comparable)


def insertion_sort(data: list[A]):
    for i in range(len(data)):
        j: int = i
        while j > 0 and data[j - 1] > data[j]:
            data[j - 1], data[j] = data[j], data[j - 1]
            j -= 1

    
data = tracelist("asdfzkljaflkzjasflkzsad")

data.read_colour(lambda rc, _1, _2: f"on rgb(0,{min(255,rc*4+40)},{min(255,rc*4+40)})")
data.write_colour(lambda _1, _2, c: c)
insertion_sort(data)
console.print(data)


