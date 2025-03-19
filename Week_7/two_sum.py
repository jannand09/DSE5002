# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from collections import defaultdict

def two_sum(nums, target):
    '''
    Return the indices of two numbers in a list that add up to a target value

    Parameters
    ----------
    nums : list
        list of numbers
    target : int
        DESCRIPTION.

    Returns
    -------
    list of two integers representing indices of nums in list whose sum equals 
    the target

    '''
    hash_map = defaultdict(int)
    for i in range(len(nums)):
        hash_map[target - nums[i]] = i
    
    for key, value in hash_map.items():
        comp = (target - key)
        if comp in hash_map.keys():
            if comp != key:
                return([value, hash_map[comp]])

            
print(two_sum([2,7,11,15], 9))
print(two_sum([3,2,4], 6))
print(two_sum([3,3], 6))