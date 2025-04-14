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


# colors are here https://rich.readthedocs.io/en/latest/appendix/colors.html
DEFAULT_WRITE_COLOR = "green3"
DEFAULT_READ_COLOR = "magenta3"
DEFAULT_NON_FOCUS_COLOR = "grey15"
DEFAULT_LIST_INDEX_COLOR = "grey50"


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
    
    def __init__(self, src: Optional[Iterable] = None, str_resets_colors: bool = True, write_color: str = DEFAULT_WRITE_COLOR, read_color: str = DEFAULT_READ_COLOR, focus: Optional[HasContains] = None):

        # create the list with any iterable
        if src:
            super().__init__(src)
        else:
            super().__init__()

        self.write_color(write_color)
        self.read_color(read_color)
        self._str_resets_colors: bool = str_resets_colors

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

        if self._read_color:
            if isinstance(i, slice):
                for j in self._slice_to_range(i):
                    self._changes[j] = self._read_color
            else:
                self._changes[i % len(self)] = self._read_color
                
        return v

    def __setitem__(self, i, v):
        super().__setitem__(i, v)
        if self._write_color:
            if isinstance(i, slice):
                for j in self._slice_to_range(i):
                    self._changes[j] = self._write_color
            else:        
                self._changes[i % len(self)] = self._write_color
        
    def reset_colors(self):
        self._changes = {}


    def focus(self, focus: Optional[HasContains]):
        self._focus = focus

        
    def write_color(self, color: str):
        self._write_color = color

        
    def read_color(self, color: str):
        self._read_color = color

        
    def __rich__(self):

        table = Table(box=LIST, show_header=False, show_footer=False)
        
        for i in range(len(self)):
            table.add_column(str(i))
        
        line: list[str] = []
        for i, x in enumerate(self):

            tmp: str = str(x)
            if self._focus and i not in self._focus:
                tmp = f"[{DEFAULT_NON_FOCUS_COLOR}]{tmp}[/{DEFAULT_NON_FOCUS_COLOR}]"
            elif i in self._changes:
                tmp = f"[{self._changes[i]}]{tmp}[/{self._changes[i]}]"

            line.append(tmp)
       
        table.add_row(*line)
        table.add_section()
        table.add_row(*map(lambda x: f"[{DEFAULT_LIST_INDEX_COLOR}]{x}[/{DEFAULT_LIST_INDEX_COLOR}]", range(len(self))))
        
        if self._str_resets_colors:
            self.reset_colors()
        
        return table

