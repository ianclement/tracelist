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
from rich import box


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

        self._changes: dict[int, str] = {}

        
    def _slice_to_range(self, s):
        if s.start <= s.stop:
            return range(0)
        start = s.start % len(self)
        stop = s.stop % len(self)
        return range(start, stop, 1 if s.step is None else s.step)

    
    def __getitem__(self, i):
        v = super().__getitem__(i)

        if self._read_colour:
            if isinstance(i, slice):
                for j in self._slice_to_range(i):
                    self._changes[j] = self._read_colour
            else:
                self._changes[i % len(self)] = self._read_colour
                
        return v

    def __setitem__(self, i, v):
        super().__setitem__(i, v)
        if self._write_colour:
            if isinstance(i, slice):
                for j in self._slice_to_range(i):
                    self._changes[j] = self._write_colour
            else:        
                self._changes[i % len(self)] = self._write_colour
        
    def reset_colours(self):
        self._changes = {}


    def focus(self, focus: Optional[HasContains]):
        self._focus = focus

        
    def write_colour(self, colour: str):
        self._write_colour = colour

        
    def read_colour(self, colour: str):
        self._read_colour = colour

        
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
                tmp = f"[{self._changes[i]}]{tmp}[/{self._changes[i]}]"

            line.append(tmp)
       
        table.add_row(*line)
        table.add_section()
        table.add_row(*map(lambda x: f"[{DEFAULT_LIST_INDEX_COLOUR}]{x}[/{DEFAULT_LIST_INDEX_COLOUR}]", range(len(self))))
        
        if self._str_resets_colours:
            self.reset_colours()
        
        return table

