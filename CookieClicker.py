"""Comparison of different strategies in the game Cookie Clicker."""

LINK = "http://www.codeskulptor.org/#user47_7OVyBKyfnK_27.py"

import math
import simpleplot
import poc_simpletest
import codeskulptor
import poc_clicker_provided as provided


# Constants
SIM_TIME = 10000000000.0
codeskulptor.set_timeout(20)


# game state class
class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        """
        Initializes the Cookie Cliker
        """
        self._current_cookies = 0.0
        self._current_cps = 1.0
        self._current_time = 0.0
        self._total_cookies = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return the state of game of the form:
        (time, current_cps, current_cookies, total_cookies)
        """
        game_state = [self._current_time, self._current_cps,
                      self._current_cookies, self._total_cookies]
        return str(game_state)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cookies:
            time_to_wait = 0.0
        else:
            time_to_wait = (cookies - self._current_cookies) / self._current_cps

        return math.ceil(time_to_wait)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return

        self._current_cookies += self._current_cps * time
        self._total_cookies += self._current_cps * time
        self._current_time += time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies < cost:
            return

        self._current_cookies -= cost
        self._current_cps += additional_cps
        self._history.append((self._current_time, item_name,
                              cost, self._total_cookies))


# simulation function
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    info_object = build_info.clone()
    clicker = ClickerState()

    while clicker.get_time() <= duration:
        time_remaining = duration - clicker.get_time()
        item_to_buy = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(),
                               time_remaining, info_object)
        if item_to_buy == None:
            break

        time_to_wait = clicker.time_until(info_object.get_cost(item_to_buy))

        if time_to_wait + clicker.get_time() > duration:
            break
        else:
            clicker.wait(time_to_wait)
            clicker.buy_item(item_to_buy, info_object.get_cost(item_to_buy),
                             info_object.get_cps(item_to_buy))
            info_object.update_item(item_to_buy)

    # accumulating cookies after the while loop ends
    clicker.wait(time_remaining)
    return clicker


# strategies for simulation
def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    info_object = build_info.clone()
    items_list = info_object.build_items()
    item_to_buy = None
    min_cost = float("inf")

    for item in items_list:
        item_cost = info_object.get_cost(item)
        if (item_cost - cookies) / cps > time_left:
            continue
        elif item_cost < min_cost:
            min_cost = item_cost
            item_to_buy = item

    return item_to_buy

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    info_object = build_info.clone()
    items_list = info_object.build_items()
    item_to_buy = None
    max_cost = float("-inf")

    for item in items_list:
        item_cost = info_object.get_cost(item)
        if (item_cost - cookies) / cps > time_left:
            continue
        elif item_cost > max_cost:
            max_cost = item_cost
            item_to_buy = item

    return item_to_buy

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    Always buy the item offering the lowest cost per cps in the time left.
    """
    info_object = build_info.clone()
    items_list = info_object.build_items()
    item_to_buy = None
    min_cost_per_cps = float("inf")

    for item in items_list:
        item_cost = info_object.get_cost(item)
        item_cps = info_object.get_cps(item)
        item_cost_per_cps = item_cost / item_cps
        if (item_cost - cookies) / cps > time_left:
            continue
        elif item_cost_per_cps < min_cost_per_cps:
            min_cost_per_cps = item_cost_per_cps
            item_to_buy = item

    return item_to_buy


# testing how strategies fare
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    history = state.get_history()
    history = [(math.log(item[0]), math.log(item[3])) for item in history]
    return history

def run():
    """
    Run the simulator.
    """
    cursor_broken = run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    cheap = run_strategy("Cheap", SIM_TIME, strategy_cheap)
    expensive = run_strategy("Expensive", SIM_TIME, strategy_expensive)
    best = run_strategy("Best", SIM_TIME, strategy_best)

    simpleplot.plot_lines("Comparison of strategies", 1000, 400, 'Time', 'Total Cookies',
                          [cursor_broken, cheap, expensive, best], True,
                          ["cursor_broken", "cheap", "expensive", "best"])

run()


# testing the ClickerState class
def run_suite(GameClass):
    """
    Some informal testing code
    """

    # creating a TestSuite object
    clicker = GameClass()
    suite = poc_simpletest.TestSuite()

    # testing the __init__() and __str__() methods
    suite.run_test(str(clicker), str([0.0, 1.0, 0.0, 0.0]), "Test #1.1: init.")
    suite.run_test(clicker.get_history(), [(0.0, None, 0.0, 0.0)], "Test 1.2: get_history")

    # testing the wait method
    clicker.wait(-1)
    suite.run_test(str(clicker), str([0.0, 1.0, 0.0, 0.0]), "Test #2.1: wait.")

    clicker.wait(0)
    suite.run_test(str(clicker), str([0.0, 1.0, 0.0, 0.0]), "Test #2.2: wait.")

    clicker.wait(530)
    suite.run_test(str(clicker), str([530.0, 1.0, 530.0, 530.0]), "Test #2.3: wait.")

    clicker.wait(10.5)
    suite.run_test(str(clicker), str([540.5, 1.0, 540.5, 540.5]), "Test #2.4: wait.")

    clicker.buy_item("Tester #1", 500, 3.0)
    clicker.wait(10.5)
    suite.run_test(str(clicker), str([551.0, 4.0, 82.5, 582.5]), "Test #2.5: wait.")

    # testing the time_until() method
    suite.run_test(clicker.time_until(100), 5.0, "Test #3.1: time_until.")
    suite.run_test(clicker.time_until(80), 0.0, "Test #3.2: time_until.")
    suite.run_test(clicker.time_until(82.5), 0.0, "Test #3.3: time_until.")
    suite.run_test(clicker.time_until(83), 1.0, "Test #3.4: time_until.")

    # testing the buy_item() method
    clicker.buy_item("Tester #2", 83, 1.5)
    history_lst = [(0.0, None, 0.0, 0.0), (540.5, "Tester #1", 500, 540.5)]
    suite.run_test(clicker.get_history(), history_lst, "Test #4.1: buy_item.")
    suite.run_test(str(clicker), str([551.0, 4.0, 82.5, 582.5]), "Test #4.2: buy_item.")

    clicker.wait(50)
    clicker.buy_item("Tester #3", 42.5, 2)
    history_lst.append((601.0, "Tester #3", 42.5, 782.5))
    suite.run_test(clicker.get_history(), history_lst, "Test #4.3: buy_item.")
    suite.run_test(str(clicker), str([601.0, 6.0, 240.0, 782.5]), "Test 4.4: buy_item.")

    # one more test of time_until
    suite.run_test(clicker.time_until(480.0), 40.0, "Test 4.5 time_until.")

    # reporting the results of the test
    suite.report_results()

run_suite(ClickerState)

