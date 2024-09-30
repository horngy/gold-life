"""
This module stores Mode2Navigator class
"""

from landsites import Land
from data_structures.hash_table import *
from data_structures.heap import *

__author__ = "Teh Yee Hong"

class Mode2Navigator:
    """
    Mode2Navigator is a class representing a navigation system for adventurers to play in mode 2

    Approach:   The data structure I used in this task is a HashTable and a MaxHeap, a HashTable is used first to store the sites
                as it can handle unique names easily, a MaxHeap is also used as it allow fast access to top data. A python inbuilt
                list is also used to return specific item required in simulate_data.
                An example for this class:
                    a = Land("A", 400, 100)
                    b = Land("B", 300, 150)
                    c = Land("C", 100, 5)
                    d = Land("D", 350, 90)
                    e = Land("E", 300, 100)
                    sites = [
                        a, b, c, d, e
                    ]
                    nav = Mode2Navigator(3)
                    nav.add_sites(sites)
                The sites will be added to the HashTable only in this stage.
                    print(nav.simulate_day(200))
                Then when this is called, it will simulate a day and return
                    [(Land(name='A', gold=0, guardians=0), 100), (Land(name='D', gold=0, guardians=0), 90), (Land(name='C', gold=0, guardians=0), 5)]
                as there are only 3 adventure teams in this example.

                Explaination of complexities are stated under each method
    """

    def __init__(self, n_teams: int) -> None:
        """
        This function helps to initialize this class

        param arg1: number of teams to explore

        Complexity: O(1)
        """
        self.teams = n_teams
        self.sites = LinearProbeTable()

    def add_sites(self, sites: list[Land]) -> None:
        """
        This function helps to store all the sites in a LinearProbeTable

        Approach:   Since we cannot assume the score of each landsites are unique, I decided to store each of them using their names.
                    A LinearProbeTable is used for its simplicity

        Example:    nav.add_sites([Land("A", 800, 100)])
                    The complexity would be O(n) since the list is not empty
                    nav.add_sites([])
                    The complexity would be O(1)

        param arg1: a list of the land to be added

        Complexity: Worst case is O(n) since setitem is O(1) in this task
                    Best case is O(1) when sites list is empty, doing nothing
        """
        for x in sites:
            self.sites[x.get_name()] = x

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        This function will simulate a day in the game, showing the best choice of each adventure team based on their team size

        Approach:   I will firstly create a MaxHeap with sorted value by calling construct_score_data_structure, then i will loop
                    through the number of teams available to calculate how much value they can gain by not exploring and by exploring.
                    Lastly will choose the choice with a better value. If they choose not to go, the land will be added back into the
                    MaxHeap, if they choose to go, the site will be calculated to see if there is still gold left in the site, if there is
                    it will be added back to the MaxHeap, or else won't.

        Example:    When this is called
                    print(nav.simulate_day(200))
                    and self.sites is not empty, the complexity would be O(n + klog(n)) as it will loop through the hash table to append it
                    into a temporary list and then to MaxHeap. And then looping through the numbers of adventure team to make a decision for each
                    team.
                    But when self.sites is empty and the number of adventure teams is 0, the complexity would be O(1) as there would be no loop of
                    HashTable and nothing into the MaxHeap, there would also be no need of looping adventure teams.

        param arg1: The adventure size

        Returns:    A list of choice made by each adventure team

        Complexity: Worst case is O(n + n + klog(n)) = O(n + klog(n)) where k is the number of adventure team participated.
                    This will occur when self.sites not empty and every team decided to explore landsites instead of not doing
                    anything.
                    Best case is O(1) when self.sites is empty and self.teams is 0, it will just return an empty list
        """
        def construct_score_data_structure(adventure_size):
            """
            This function helps to create a usable data structure with the sorted value of sites

            Approach:   Firstly i will add every sites that still have gold into a temperorary list, i will also calculate
                        its value at the same time so that the next step, adding it into a MaxHeap will sort it out. A MaxHeap
                        is also used here since it allow easy and fast access to the greatest element (get_max()).

            param arg1: The adventure size so that the value of each site could be calculated

            Return:     a MaxHeap

            Complexity: Worst case is O(n) as O(n+n) = O(2n) = O(n). This will occur when self.sites (hash table) is not empty
                        Best case is O(1) as if self.sites is empty, the temporary list will be empty too, the MaxHeap will also be
                        empty
            """
            temp1 = []
            for x in self.sites.values():  # n
                if x.get_gold() != 0:  # if there's no gold left there is no point of taking the place
                    value, sended, gold_left = helper(adventure_size, x)
                    temp1.append((value, x, sended, gold_left))
            return MaxHeap.heapify(temp1)  # n

        def helper(adventure_size, land):
            """
            This function helps to calculate the value of each sites

            Approach:   It will calculate the value of each sites based on the given adventure size

            param arg1: the adventure size in integer
            param arg2: the site to be calculated

            Returns:    the value of the sites,
                        the adventure team size that is needed to explore the site
                        the gold left in the site after exploring

            Complexity: Both cases are O(1) as there are only calculations
            """
            if adventure_size >= land.get_guardians():
                value = 2.5 * (adventure_size - land.get_guardians()) + land.get_gold()
                return value, land.get_guardians(), 0
            else:
                value = min(adventure_size * land.get_gold() / land.get_guardians(), land.get_gold())
                return value, adventure_size, land.get_gold() - value

        heap = construct_score_data_structure(adventurer_size)
        final_list = []
        for x in range(self.teams):  # k
            if_no_go = 2.5 * adventurer_size + 0
            data = heap.get_max()  # logn
            if if_no_go > data[0]:
                final_list.append((None, 0))
                heap.add(data)  # logn  adding back into the MaxHeap
            else:
                land, sended, gold_left = data[1], data[2], data[3]
                land.set_gold(gold_left)
                land.set_guardians(land.get_guardians() - sended)
                new_value, new_sended, new_gold_left = helper(adventurer_size, land)  # calculate new value
                final_list.append((land, sended))
                self.sites[land.get_name()] = land  # change the data in the HashTable
                if gold_left != 0:
                    heap.add((new_value, land, new_sended, new_gold_left))  # log n  adding back to the MaxHeap
        return final_list

