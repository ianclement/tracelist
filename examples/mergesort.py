from typing import TypeVar, Optional, Protocol
from tracelist import tracelist

from rich import print


class Comparable(Protocol):
    def __lt__(self, other) -> bool:
        pass

A = TypeVar("A", bound=Comparable)


def merge(src: list[A], low: int, mid: int, high: int, dst: list[Optional[A]]):
    """Merge src[low:mid] with src[mid+1:high] into dst[low:high].
       Assumes that src[low:mid] and src[mid+1:high] are individually sorted when this is called"""
    i: int = low
    j: int = mid + 1

    for k in range(low, high + 1):
        if i > mid:
            dst.write_color("cornflower_blue")
            dst[k] = src[j]
            j += 1
        elif j > high:
            dst.write_color("green3")
            dst[k] = src[i]
            i += 1
        elif src[i] < src[j]:
            dst.write_color("green3")
            dst[k] = src[i]
            i += 1
        else:
            dst.write_color("cornflower_blue")
            dst[k] = src[j]
            j += 1

def mergesort(xs: list[A]):
    buffer: list[A] = [None] * len(xs)
    mergesort_h(xs, 0, len(xs) - 1, buffer, 1)

    
def mergesort_h(xs: tracelist[A], low: int, high: int, buffer: tracelist[Optional[A]], depth):

    print(f"{'*' * depth} mergesort_h(xs, {low}, {high}, buffer)")
    
    if low >= high:
        print(f"{'*' * depth} nothing to do!")
        return

    # sort the two evenly divied subarrays 
    mid: int = (low + high) // 2
    mergesort_h(xs, low, mid, buffer, depth + 1)
    mergesort_h(xs, mid + 1, high, buffer, depth + 1)

    # copy the sub-arrays into the buffer

    xs.read_color("green3")
    for i in range(low, high + 1):
        if i == (low + high) // 2 + 1:
            xs.read_color("cornflower_blue")
        buffer[i] = xs[i]
    xs.read_color(None)

    xs.focus(range(low, high + 1))

    print(f"{'*' * depth} Before merge:")
    print(xs)
        
    # merge back into xs, so now xs[low:high] is now sorted
    merge(buffer, low, mid, high, xs)

    print(f"{'*' * depth} After merge:")
    print(xs)
    print(f"{'*' * depth} Done merge!")
    
# [5,3,6,4,9,7,4,5,3,4,1,4,3,7]
data = tracelist("asdfzkljaflkzjasflkzsad", read_color=None)
mergesort(data)
print(data)
