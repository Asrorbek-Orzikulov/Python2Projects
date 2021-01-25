"""Code for Word Wrangler game."""

LINK = "http://www.codeskulptor.org/#user48_SIF9V4mwDi_14.py"

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

codeskulptor.set_timeout(60)
WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) <= 1:
        return list1

    from_second_unique = [list1[idx] for idx in range(1, len(list1)) \
                          if list1[idx] != list1[idx - 1]]
    return [list1[0]] + from_second_unique

def is_in(item, a_list):
    """
    Checks whether the item is in the ordered
    list a_list using a binary search.

    Returns Boolean.
    """
    if len(a_list) == 0:
        return False
    elif len(a_list) == 1:
        return item == a_list[0]
    else:
        if item < a_list[len(a_list) / 2]:
            return is_in(item, a_list[: len(a_list) / 2])
        else:
            return is_in(item, a_list[len(a_list) / 2 : ])

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection = [elem for elem in list2 if is_in(elem, list1)]
    return intersection

# Functions to perform merge sort
def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function is iterative.
    """
    first_list = list(list1)
    second_list = list(list2)
    merged_list = []

    # iterating until one of the lists is empty
    while (len(first_list) > 0) and (len(second_list) > 0):
        if first_list[0] < second_list[0]:
            merged_list.append(first_list.pop(0))
        else:
            merged_list.append(second_list.pop(0))

    # appending the rest of the non-empty list
    if len(first_list) == 0:
        merged_list.extend(second_list)
    elif len(second_list) == 0:
        merged_list.extend(first_list)

    return merged_list

def merge1(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function is recursive.
    """
    first_list = list(list1)
    second_list = list(list2)

    # appending the rest of the non-empty list
    if len(first_list) == 0:
        return second_list
    elif len(second_list) == 0:
        return first_list

    # merging the list recursively
    else:
        if first_list[0] < second_list[0]:
            rest_merged = merge1(first_list[1: ], second_list)
            return [first_list[0]] + rest_merged
        else:
            rest_merged = merge1(first_list, second_list[1: ])
            return [second_list[0]] + rest_merged

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    unsorted_list = list(list1)
    if len(unsorted_list) <= 1:
        return unsorted_list
    else:
        first_half_sorted = merge_sort(unsorted_list[: len(unsorted_list) / 2])
        second_half_sorted = merge_sort(unsorted_list[len(unsorted_list) / 2 :])
        return merge(first_half_sorted, second_half_sorted)

# Function to rearrange the elements of a string
def rearrange(letter, string, pos):
    """
    Function that generates new strings by inserting
    the letter in all possible positions within the string.

    Returns a list with new strings.
    """
    if pos == len(string):
        return [string + letter]
    else:
        current_word = string[: pos] + letter + string[pos: ]
        return [current_word] + rearrange(letter, string, pos + 1)

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    else:
        first_char = word[0]
        rest_strings = gen_all_strings(word[1: ])
        all_strings = []
        for string in rest_strings:
             all_strings += rearrange(first_char, string, 0)
        return rest_strings + all_strings

# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    return [line[: -1] for line in netfile.readlines()]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)


run()
# Informal tests of functions
class TestSuite:
    """
    Create a suite of tests similar to unittest
    """
    def __init__(self):
        """
        Creates a test suite object
        """
        self._total_tests = 0
        self._failures = 0


    def run_test(self, computed, expected, message = ""):
        """
        Compare computed and expected
        If not equal, print message, computed, expected
        """
        self._total_tests += 1
        if computed != expected:
            msg = message + " Computed: " + str(computed)
            msg += " Expected: " + str(expected)
            print msg
            self._failures += 1

    def report_results(self):
        """
        Report back summary of successes and failures
        from run_test()
        """
        msg = "Ran " + str(self._total_tests) + " tests. "
        msg += str(self._failures) + " failures."
        print msg

def run_suite():
    """
    Some informal testing code
    """

    # creating a TestSuite object
    suite = TestSuite()

    # testing the remove_duplicates function
    sorted_list1 = [1, 2, 3, 4, 4, 4, 5, 5, 6]
    suite.run_test(remove_duplicates(sorted_list1), [1, 2, 3, 4, 5, 6], "Test #1.1: remove_duplicates.")

    sorted_list2 = [-1, 2, 2, 4, 4, 4, 10, 15, 15]
    suite.run_test(remove_duplicates(sorted_list2), [-1, 2, 4, 10, 15], "Test #1.2: remove_duplicates.")

    sorted_list3 = [8, 8, 8, 8]
    suite.run_test(remove_duplicates(sorted_list3), [8], "Test #1.3: remove_duplicates.")

    sorted_list4 = []
    suite.run_test(remove_duplicates(sorted_list4), [], "Test #1.4: remove_duplicates.")

    # testing the is_in function
    suite.run_test(is_in(2, sorted_list1), True, "Test #2.1: is_in.")
    suite.run_test(is_in(3, sorted_list2), False, "Test #2.2: is_in.")
    suite.run_test(is_in(15, sorted_list2), True, "Test #2.3: is_in.")

    words = ["feared", "whaps", "wino", "writhen", "yawned", "yttrias"]
    suite.run_test(is_in("feared", words), True, "Test #2.4: is_in.")
    suite.run_test(is_in("fear", words), False, "Test #2.5: is_in.")

    words = load_words(WORDFILE)
    suite.run_test(is_in("zorilla", words), True, "Test #2.6: is_in.")
    suite.run_test(is_in("severals", words), True, "Test #2.7: is_in.")
    suite.run_test(is_in("bungling", words), True, "Test #2.8: is_in.")
    suite.run_test(is_in("bunglings", words), False, "Test #2.9: is_in.")

    # testing the intersect function
    suite.run_test(intersect(sorted_list1, sorted_list2), [2, 2, 4, 4, 4], "Test #3.1: intersection.")
    suite.run_test(intersect(sorted_list2, sorted_list1), [2, 4, 4, 4], "Test #3.2: intersection.")

    # testing the merge function
    sorted_list1 = [1, 2, 3, 4, 5, 5, 6, 15]
    sorted_list2 = [-1, 2, 2, 4, 4, 4, 10, 15, 15]
    merged_list = [-1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 6, 10, 15, 15, 15]
    suite.run_test(merge(sorted_list1, sorted_list2), merged_list, "Test #4.1: merge.")

    sorted_list1 = [1, 3, 5, 5, 7, 9, 9]
    sorted_list2 = [2, 2, 4, 6, 8, 8, 10, 10]
    merged_list = [1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 9, 9, 10, 10]
    suite.run_test(merge(sorted_list1, sorted_list2), merged_list, "Test #4.2: merge.")

    # testing the merge1 function
    sorted_list1 = [1, 2, 3, 4, 5, 5, 6, 15]
    sorted_list2 = [-1, 2, 2, 4, 4, 4, 10, 15, 15]
    merged_list = [-1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 5, 6, 10, 15, 15, 15]
    suite.run_test(merge1(sorted_list1, sorted_list2), merged_list, "Test #5.1: merge1.")

    sorted_list1 = [1, 3, 5, 5, 7, 9, 9]
    sorted_list2 = [2, 2, 4, 6, 8, 8, 10, 10]
    merged_list = [1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 9, 9, 10, 10]
    suite.run_test(merge1(sorted_list1, sorted_list2), merged_list, "Test #5.2: merge1.")

    # testing the merge_sort function
    unsorted_list = [2, 4, -1, 3]
    suite.run_test(merge_sort(unsorted_list), [-1, 2, 3, 4], "Test #6.1: merge_sort.")

    unsorted_list = [10, 4, 2, 8, 2, 6, 8, 10, -1]
    suite.run_test(merge_sort(unsorted_list), [-1, 2, 2, 4, 6, 8, 8, 10, 10], "Test #6.2: merge_sort.")

    # testing the rearrange function
    result = ["aJahongir", "Jaahongir", "Jaahongir", "Jahaongir", "Jahoangir",
              "Jahonagir", "Jahongair", "Jahongiar", "Jahongira"]
    suite.run_test(rearrange("a", "Jahongir", 0), result, "Test #7: rearrange.")

    # testing the gen_all_strings function
    result = ["", "b", "a", "ab", "ba", "a", "ab", "ba", "aa",
              "aa", "aab", "aab", "aba", "aba", "baa", "baa"]
    suite.run_test(gen_all_strings("aab"), result, "Test #8.1: gen_all_strings.")

    result1 = ["", "c", "b", "bc", "cb", "a", "ac", "ca", "ab",
              "ba", "abc", "bac", "bca", "acb", "cab", "cba"]
    suite.run_test(gen_all_strings("abc"), result1, "Test #8.2: gen_all_strings.")

    # reporting the results of the test
    suite.report_results()

#run_suite()
