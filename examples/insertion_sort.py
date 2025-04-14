# this isn't recursion just a test of the trace list

from typing import TypeVar, Optional, Protocol

from tracelist import tracelist
from rich import print


class Comparable(Protocol):
    def __lt__(self, other) -> bool:
        pass
        

A = TypeVar("A", bound=Comparable)


def insertion_sort(data: tracelist[A]):
    for i in range(len(data)):
        print(f"Sorted between {0} and {i}")
        data.focus(range(i+1))
        j: int = i
        while j > 0 and data[j - 1] > data[j]:
            data[j - 1], data[j] = data[j], data[j - 1]
            j -= 1
        print(data)

    
#data = tracelist([81, 26, 44, 99, 67, 79, 90, 64, 44, 24, 100, 64])
data = tracelist([81, 26, 44, 99, 24, 64, 79])
data.read_color(None)
insertion_sort(data)
print(data)



#data.read_color(lambda rc, _1, _2: f"on rgb(0,{min(255,rc*4+40)},{min(255,rc*4+40)})")
#data.write_color(lambda _1, _2, c: c)
