# Copyright (C) 2025. Ian Clement

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, Protocol, TypeVar, Iterable, Callable

from rich.table import Table
from rich.console import Console
from rich import box
from dataclasses import dataclass

# colours are here https://rich.readthedocs.io/en/latest/appendix/colors.html
DEFAULT_WRITE_COLOUR = "green3"
DEFAULT_READ_COLOUR = "magenta3"
DEFAULT_NON_FOCUS_COLOUR = "grey15"
DEFAULT_LIST_INDEX_COLOUR = "grey50"


LIST: box.Box = box.Box(
    "┌─┬┐\n"
    "│ ││\n"
    "╶─┼╴\n"
    "│ ││\n"
    "└─┴┘\n"
    "╶─┼╴\n"
    "    \n"  # "  ╵ \n"
    "    \n"
)

class HasContains(Protocol):
    def __contains__(self, x) -> bool:
        pass

    
@dataclass
class ReadWriteColour:
    read_count: int
    write_count: int
    colour: str = ""

    def update(self, f: Callable[[int, int, str], str]):
        self.colour = f(self.read_count, self.write_count, self.colour)

class tracelist(list):
    """A list class that traces the changes made to the list."""
    
    def __init__(self, src: Optional[Iterable] = None, str_resets_colours: bool = True, write_colour: str = DEFAULT_WRITE_COLOUR, read_colour: str = DEFAULT_READ_COLOUR, focus: Optional[HasContains] = None):

        # create the list with any iterable
        if src:
            super().__init__(src)
        else:
            super().__init__()

        self.write_colour(write_colour)
        self.read_colour(read_colour)
        self._str_resets_colours: bool = str_resets_colours

        self._focus: Optional[HasContains] = focus

        self._changes: dict[int, ReadWriteColour] = {}

    def _slice_to_range(self, s):
        if s.start <= s.stop:
            return range(0)
        start = s.start % len(self)
        stop = s.stop % len(self)
        return range(start, stop, 1 if s.step is None else s.step)

    def _update_changes_at(self, i: int, f: Callable[[int, int, str], str], read:bool):
        if i not in self._changes:
            self._changes[i] = ReadWriteColour(0, 0)
        if read:
            self._changes[i].read_count += 1
        else:
            self._changes[i].write_count += 1
        print(self._changes[i])
        self._changes[i].update(f)
    
    def __getitem__(self, i):
        v = super().__getitem__(i)

        if self._read_colour:
            if isinstance(i, slice):
                for j in self._slice_to_range(i):
                    self._update_changes_at(j, self._read_colour, True)
            else:
                self._update_changes_at(i % len(self), self._read_colour, True)

        return v

    def __setitem__(self, i, v):
        super().__setitem__(i, v)
        if self._write_colour:
            if isinstance(i, slice):
                for j in self._slice_to_range(i):
                    self._update_changes_at(j, self._write_colour, True)
            else:        
                self._update_changes_at(i % len(self), self._write_colour, True)
        
    def reset_colours(self):
        self._changes = {}


    def focus(self, focus: Optional[HasContains]):
        self._focus = focus

        
    def write_colour(self, colour: str | Callable[[int, int, str], str]):
        if callable(colour):
            self._write_colour = colour
        else:
            self._write_colour = lambda _1, _2, _3: colour
            
    def read_colour(self, colour: str | Callable[[int, int, str], str]):
        if callable(colour):
            self._read_colour = colour
        else:
            self._read_colour = lambda _1, _2, _3: colour
            
    def __rich__(self):

        table = Table(box=LIST, show_header=False, show_footer=False)
        
        for i in range(len(self)):
            table.add_column(str(i))
        
        line: list[str] = []
        for i, x in enumerate(self):

            tmp: str = str(x)
            if self._focus and i not in self._focus:
                tmp = f"[{DEFAULT_NON_FOCUS_COLOUR}]{tmp}[/{DEFAULT_NON_FOCUS_COLOUR}]"
            elif i in self._changes:
                tmp = f"[{self._changes[i].colour}]{tmp}[/{self._changes[i].colour}]"

            line.append(tmp)
        print(line)
        table.add_row(*line)
        table.add_section()
        table.add_row(*map(lambda x: f"[{DEFAULT_LIST_INDEX_COLOUR}]{x}[/{DEFAULT_LIST_INDEX_COLOUR}]", range(len(self))))
        
        if self._str_resets_colours:
            self.reset_colours()
        
        return table


if __name__ == "__main__":

    console: Console = Console()

    
    xs = tracelist("abcdefg", focus=range(1, 6), read_colour=None)

    xs[1] = "h"
    console.print(xs)
    xs[3] = xs[4]
    console.print(xs)
