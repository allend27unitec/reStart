"""
assignment 1
part 1.1
allend27
May 2024
"""
from typing import List

def transform_list(input_list: List[str]) -> List[str]:
    var: List[str] = input_list
    rvar: List[str] = var[::-1] # reverse list
    rvar = rvar[:3] + ['z'] + rvar[3:] # add 'z' at index 3
    rvar = rvar + ['o'] # append 'o'
    return rvar

if __name__ == "__main__":
    start_list: List[str] = ['a','b','c','d','e']
    result_list: List[str] = transform_list(start_list)
    print(result_list)

