"""Code for the 2048 game."""

LINK = "http://www.codeskulptor.org/#user48_akmwSi5AOM_8.py"

import random
import poc_2048_gui

# Directions and offsets for computing tile indices in each direction.
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


# helper functions
def slide(line):
    """
    Slides a line along a given dimension
    """
    shifted_list = [0] * len(line)
    for num in line:
        if num != 0:
            shifted_list[shifted_list.index(0)] = num
    return shifted_list

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    slid_line = slide(line)
    merged_line = list(slid_line)
    for ind in range(1, len(slid_line)):
          if (slid_line[ind] == slid_line[ind - 1]) and (
              slid_line[ind] == merged_line[ind - 1]):
                merged_line[ind] = 0
                merged_line[ind - 1] *= 2
    return slide(merged_line)

def find_zeros(list_of_lists, height, width):
    """
    Finds the indices of zeros in a height by width list of lists
    """
    zeros_lst = []
    for row in range(height):
        for col in range(width):
            if list_of_lists[row][col] == 0:
                zeros_lst.append([row, col])
    return zeros_lst

def traverse(start_cell, direction, num_steps):
    """
    Iterates over the cells in a grid in a linear fashion
    and forms a list of traversed elements.

    start_cell is a tuple (row, col) where the iteration starts.

    direction is a tuple that contains the difference between the
    positions of consecutive elements.
    """
    traverse_lst = []
    for step in range(num_steps):
        row = start_cell[0] + direction[0] * step
        col = start_cell[1] + direction[1] * step
        traverse_lst.append((row, col, step))
    return traverse_lst

# Class 2048
class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height_ = grid_height
        self._width_ = grid_width
        self.reset()
        self._initials_ = {UP: [(0, col) for col in range(self._width_)],
                       DOWN: [(self._height_ - 1, col) for col in range(self._width_)],
                       RIGHT: [(row, self._width_ - 1) for row in range(self._height_)],
                       LEFT: [(row, 0) for row in range(self._height_)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._board_ = [[0 for dummy_col in range(self._width_)]
                        for dummy_row in range(self._height_)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board_)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height_

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width_

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        self._changed_ = False
        num_steps = len(self._initials_[(direction + 1) % 4 + 1])

        for initial in self._initials_[direction]:
            pre_merge_lst = [self.get_tile(row, col)
                             for row, col, dummy_step in traverse(initial, OFFSETS[direction], num_steps)]
            merged_lst = merge(pre_merge_lst)

            if pre_merge_lst != merged_lst:
                self._changed_ = True
                for row, col,step in traverse(initial, OFFSETS[direction], num_steps):
                    self.set_tile(row, col, merged_lst[step])

        if self._changed_:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile_num = random.choice([2] * 9 + [4] * 1)
        zero_ind = random.choice(find_zeros(self._board_, self._height_, self._width_))
        self._board_[zero_ind[0]][zero_ind[1]] = tile_num

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board_[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board_[row][col]


#gui for the 2048
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
