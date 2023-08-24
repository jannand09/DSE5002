
from collections import defaultdict

def find_palindrome(str):
    reverse_list = []
    for i in range(len(str)-1, -1, -1):
        reverse_list.append(str[i])
    
    reverse_str = "".join(reverse_list)

    return str == reverse_str


def find_palindrome_again(str):
    str_list = list(str) # [x for x in str] 

    i = 0
    j = len(str_list) - 1
    while i < j:
        temp = str_list[i]
        str_list[i] = str_list[j]
        str_list[j] = temp
        i = i + 1
        j = j - 1
    
    reverse_str = "".join(str_list)

    return str == reverse_str


def two_sum(nums, target):
    hash_map = defaultdict(int)
    for i in range(len(nums)):
        hash_map[target - nums[i]] = i
    
    for key, value in hash_map.items():
        comp = (target - key)
        if comp in hash_map.keys():
            if comp != key:
                return([value, hash_map[comp]])


print(two_sum([2,7,11,15], 9))
print("-----------")
print(two_sum([3,2,4], 6))
print("-----------")
print(two_sum([3,3], 6))

'''print(find_palindrome("rotator"))
print(find_palindrome("palindrome"))
print(find_palindrome("noon"))

print(find_palindrome_again("rotator"))
print(find_palindrome_again("palindrome"))
print(find_palindrome_again("noon")) '''