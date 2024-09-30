"""
This module stores Mode1Navigator class
"""

from landsites import Land
from data_structures.bst import *

__author__ = "Teh Yee Hong"

class Mode1Navigator:
    """
    Mode1Navigator is a class representing a navigation system for adventurers to play in mode 1

    Approach:   The data structure I used to store the sites is a Binary Search Tree as it is efficient in sorting the sites. I first will calculate
                the value of each sites then only insert it into the BST. Python inbuilt list is also used to return specific items required by different
                methods in this class. An example would be something like:
                    a = Land("A", 400, 100)
                    b = Land("B", 300, 150)
                    c = Land("C", 100, 5)
                    d = Land("D", 350, 90)
                    e = Land("E", 300, 100)
                    sites = [
                        Land(a.get_name(), a.get_gold(), a.get_guardians()),
                        Land(b.get_name(), b.get_gold(), b.get_guardians()),
                        Land(c.get_name(), c.get_gold(), c.get_guardians()),
                        Land(d.get_name(), d.get_gold(), d.get_guardians()),
                        Land(e.get_name(), e.get_gold(), e.get_guardians()),
                    ]
                    nav = Mode1Navigator(sites, 200)
                where there is a total of 5 sites and 200 adventurers. Then specific method would be like:
                    nav.select_sites() to return the final list of the sites in order, or gold earned
                    nav.select_sites_from_adventure_numbers([0, 200, 500, 300, 40]) to return the final list containing gold earnable based on the number of adventurer
                    nav.update_site(sites[0], 300, 1) to update the first site

                Explanation of complexities result are stated on each method
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        This function helps to initialize this class

        Approach:   The data structure I used to store the sites is a Binary Search Tree as it is efficient in sorting the sites. I first will calculate
                    the value of each sites then only insert it into the BST.

        Example:    nav = Mode1Navigator(sites, 200) and sites would be something like
                    a = Land("A", 400, 100)
                    b = Land("B", 300, 150)
                    c = Land("C", 100, 5)
                    d = Land("D", 350, 90)
                    e = Land("E", 300, 100)
                    sites = [
                        Land(a.get_name(), a.get_gold(), a.get_guardians()),
                        Land(b.get_name(), b.get_gold(), b.get_guardians()),
                        Land(c.get_name(), c.get_gold(), c.get_guardians()),
                        Land(d.get_name(), d.get_gold(), d.get_guardians()),
                        Land(e.get_name(), e.get_gold(), e.get_guardians()),
                    ]
                    In this way the complexity would be O(nlog(n)) as the list is not empty, and all sites will be inserted into the BST one by one.
                    if sites = [] and nav = Mode1Navigator(sites, 200)
                    the complexity would be O(1) as the list is empty and loop will not take place

        param arg1: list of sites to be added
        param arg2: number of adventurers to explore

        Complexity: Worst case is O(nlog(n)), looping the list of sites, then adding them into a binary search tree based on their value.
                    Best case is O(1), when list of sites is empty, the loop will not take place
        """
        self.adventurers = adventurers

        self.sites = BinarySearchTree()
        for x in sites:  # n
            value = x.get_gold() / x.get_guardians()
            self.sites[value] = x  # logn since the depth of BST is bound by O(logn)

    def select_sites(self, adventurer=None, gold_need=False) -> list[tuple[Land, int]]:
        """
        This function helps to select the best choice of sites to maximise the value and also the gold to be earned.

        Approach:   Having the adventurer and gold_need parameter helps to solve select_sites_from_adventure_numbers easier,
                    keeping track of both final list and gold earned. This method will call on select_sites_aux method to help
                    solve the problem, it will first look at the root of the BST, then always go the right side of the tree,
                    since it will always have a higher value, and take the parent tree when there is no more right.

        Example:    if the sites is from the example __init__ above, (the not empty one)
                    nav.select_sites() will return a sorted list of best valued sites
                    nav.select_sites(x, True) and x could be any adventurers count, it will return the gold earnable based
                    on the value of x
                    Best case situation example is nav.select_sites(0), where adventurer is now 0, select_sites_aux will end straight
                    away and the complexity is O(1)

        param arg1: adventurers to explore, if nothing then it will be automatically select self. adventurers
        param arg2: boolean to choose to return the gold earnable or not

        Return:     Either the final list of the sites in order, or gold earned

        Complexity: This is dependent on select_sites_aux
                    Worst case is O(N), if the count is not 0 and root(node) is not None, it will keep on looping until it reaches
                    the end of the BST or adventurers count reach 0
                    Best case is O(1), when the count is 0 or root(node) is None, the loop will not even start
        """
        final_list = []
        gold = 0

        def select_sites_aux(root, count, gold):
            """
            This function helps to update the list to be attack and the gold to be earned

            param arg1: The node in the bst (the site)
            param arg2: current adventurers count, if 0 will end
            param arg3: current gold count, to keep track of the gold earned

            Returns: adventurers count and gold earned

            Complexity: Worst case is O(N), if the count is not 0 and root(node) is not None, it will keep on looping until it reaches
                        the end of the BST or adventurers count reach 0
                        Best case is O(1), when the count is 0 or root(node) is None, the loop will not even start
            """
            if root is None or count == 0:
                return count, gold
            count, gold = select_sites_aux(root.right, count, gold)
            if count >= root.item.get_guardians():
                gold += root.item.get_gold()
                final_list.append((root.item, root.item.get_guardians()))
                count -= root.item.get_guardians()
            else:
                gold += min(root.item.get_gold() * count / root.item.get_guardians(), root.item.get_gold())
                final_list.append((root.item, count))
                count = 0
                return count, gold
            return select_sites_aux(root.left, count, gold)

        if adventurer is None:
            adventurer = self.adventurers

        count, gold = select_sites_aux(self.sites.root, adventurer, gold)
        if gold_need is False:
            return final_list
        else:
            return gold

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        This function will calculate the maximum gold earnable based on the number of adventurer

        Approach:   I will first loop the list of adventure_numbers, getting each of the value (number of adventurer) and use select_sites with gold_need to be true
                    to calculate gold earnable based on the number of adventurer, then only append it into the final list

        Example:    nav.select_sites_from_adventure_numbers([0, 200, 500, 300, 40])
                    Since the list is not empty, the complexity will be O(A * N) as it will have to calculate one by one to be appended into the final list
                    nav.select_sites_from_adventure_numbers([])
                    Since the list is empty, the complexity will be O(1) as it will only return an empty list

        param arg1: the list of adventurers number to explore

        Return:     a final list containing gold earnable based on the number of adventurer

        Complexity: Worst case is O(A * N) where A is the length of adventuer_numbers, it will have to loop through the entire list of adventure_number
                    and call select_sites with gold_need is True to return a gold value to be appended into final list, the complexity of select_sites is O(N)
                    Best case is O(1) when the adventure_numbers list is empty, nothing to loop, nothing will happen, returning an empty final list
        """
        final_list = []
        for x in adventure_numbers:  # A
            final_list.append(self.select_sites(x, True))  # N
        return final_list

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        This functions help to update the rewards and guardians of a land

        Approach:   Calculate the old value of the land and if the land does not exist, will raise ValueError, else will
                    delete the old site and add in the new site with new reward and guardians

        Example:    nav.update_site(sites[0], 300, 1) from the example __init__ above (non-empty one)
                    it will become Land("A", 300, 1)
                    if it is something like nav.update_site(f, 300, 1), where f does not exist in the sites,
                    ValueError will be raised

        param arg1: the land to be updated
        param arg2: the new value of reward
        param arg3: the new value of guardians

        Complexity: Best and worst case is O(log(n)), where O(log(n) + log(n)) = O(2log(n))
                    if the site cannot be found will raise ValueError
        """
        value = land.get_gold() / land.get_guardians()
        new = Land(land.get_name(), new_reward, new_guardians)
        new_value = new.get_gold() / new.get_guardians()
        del self.sites[value]  # log n
        self.sites[new_value] = new  # log n
