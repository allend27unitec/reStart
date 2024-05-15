"""
assignment 1
part 1.2
allend27
May 2024
"""
from typing import List, Dict

def convert(keys:str, values:int) -> Dict:
    # Ensure both lists have the same length
    if len(keys) != len(values):
        raise ValueError("Lists must have the same length")

    # Create a dictionary using a dictionary comprehension
    return {key: value * 100 for key, value in zip(keys, values)}

if __name__ == '__main__':
    strKeyList: List[str] = ['a', 'b', 'c']
    intValueList: List[int] = [1, 2, 3]
    dictResult: Dict[str, int] = convert(strKeyList, intValueList)
    print("Dictionary from associated key/value lists: ", dictResult)
