"""A simple Zombie Apocalypse mini-project."""

LINK = "http://www.codeskulptor.org/#user48_tXLNGM8mHj_24.py"

import random
import poc_grid
import poc_queue
import poc_zombie_gui
import poc_simpletest

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)

        if obstacle_list != None:
            self._obtacle_list = obstacle_list
            for cell in self._obtacle_list:
                self.set_full(cell[0], cell[1])
        else:
            self._obtacle_list = []

        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []

        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def __str__(self):
        """
        Return a human readable representation of
        human, zombie and obstacles lists
        """
        string_list = ""
        string_list += "Obstacle list is: " + str(self._obtacle_list)
        string_list += "\n"
        string_list += "Zombie list is: " + str(self._zombie_list)
        string_list += "\n"
        string_list += "Human list is: " + str(self._human_list)
        return string_list

    def show_cells(self):
        """
        Get the indexes of empty cells
        """
        cell_list = [cell for cell in self._cells]
        return cell_list

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        self._obtacle_list = []
        poc_grid.Grid.clear(self)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        entity_dict = {HUMAN : self._human_list, ZOMBIE : self._zombie_list}
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width \
                          for dummy_col in range(self._grid_width)] \
                          for dummy_row in range(self._grid_height)]

        # creating a boundary for the breadth-first search
        boundary = poc_queue.Queue()
        for entity in entity_dict[entity_type]:
            boundary.enqueue(entity)
            distance_field[entity[0]][entity[1]] = 0
            visited.set_full(entity[0], entity[1])

        # execution of the breadth-first search
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])

            for neighbor in neighbors:
                if neighbor in self._obtacle_list:
                    continue
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    boundary.enqueue(neighbor)

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_list = self._human_list
        distance_field = list(zombie_distance_field)

        for idx, human in enumerate(human_list):
            possible_moves = [human] + self.eight_neighbors(human[0], human[1])
            move_payoff = [(distance_field[move[0]][move[1]], move) \
                           for move in possible_moves \
                           if self.is_empty(move[0], move[1])]

            best_moves = [payoff[1] for payoff in move_payoff \
                          if payoff[0] == max(move_payoff)[0]]

            self._human_list[idx] = random.choice(best_moves)

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_list = self._zombie_list
        distance_field = list(human_distance_field)

        for idx, zombie in enumerate(zombie_list):
            possible_moves = [zombie] + self.four_neighbors(zombie[0], zombie[1])
            move_payoff = [(distance_field[move[0]][move[1]], move) \
                           for move in possible_moves \
                           if self.is_empty(move[0], move[1])]

            best_moves = [payoff[1] for payoff in move_payoff \
                          if payoff[0] == min(move_payoff)[0]]

            self._zombie_list[idx] = random.choice(best_moves)


poc_zombie_gui.run_gui(Apocalypse(30, 40))


# testing the Apocalypse class
def run_suite(GameClass):
    """
    Some informal testing code
    """

    # creating a TestSuite object
    suite = poc_simpletest.TestSuite()

    # testing the __init__() and show_cells() methods
    game = GameClass(5, 5, obstacle_list = [(2, 1), (0, 3)], \
                     zombie_list = [(1, 3), (3, 0)], \
                     human_list = [(2, 0), (3, 3)])

    game_state = [[0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]

    suite.run_test(game.show_cells(), game_state, "Test #1: init.")
    print game
    print

    # testing the clear() method
    game.clear()
    game_state = [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]

    suite.run_test(game.show_cells(), game_state, "Test #2: clear.")
    print game
    print

    # testing the add_zombie() and num_zombies() methods
    game = GameClass(5, 5, obstacle_list = [(2, 1), (1, 4), (0, 1)])
    game.add_zombie(3, 4)
    game.add_zombie(4, 1)
    suite.run_test(game.num_zombies(), 2, "Test #3.1: num_zombies.")
    game.add_zombie(1, 1)
    suite.run_test(game.num_zombies(), 3, "Test #3.2: num_zombies.")
    print game
    print

    # testing the add_human() and num_humans() methods
    game.add_human(0, 3)
    suite.run_test(game.num_humans(), 1, "Test #4.1: num_humans.")
    game.add_human(2, 2)
    suite.run_test(game.num_humans(), 2, "Test #4.2: num_humans.")
    print game
    print

    # testing the compute_distance_field() method
    human_distance_field = [[4, 25,  1,  0,  1],
                            [3,  2,  1,  1, 25],
                            [4, 25,  0,  1,  2],
                            [3,  2,  1,  2,  3],
                            [4,  3,  2,  3,  4]]

    suite.run_test(game.compute_distance_field(HUMAN), human_distance_field, "Test 5.1: distance field.")

    zombie_distance_field = [[2, 25,  2,  3,  4],
                             [1,  0,  1,  2, 25],
                             [2, 25,  2,  2,  1],
                             [2,  1,  2,  1,  0],
                             [1,  0,  1,  2,  1]]

    suite.run_test(game.compute_distance_field(ZOMBIE), zombie_distance_field, "Test 5.2: distance field.")

    # testing the move_humans() method
    game = GameClass(5, 5, obstacle_list = [(2, 1), (1, 4), (0, 1)], \
                     zombie_list = [(4, 4), (1, 3), (3, 4), (1, 1), (3, 3)],
                     human_list = [(0, 0), (1, 3), (3, 4), (1, 1), (3, 3)])

    game.move_humans(zombie_distance_field)
    game.move_zombies(human_distance_field)
    print game
    print

    # reporting the results of the test
    suite.report_results()


#run_suite(Apocalypse)
