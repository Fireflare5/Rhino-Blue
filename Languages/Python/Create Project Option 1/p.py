from typing import List
def allPositive(myList: List[int]) -> bool:
    for val in myList:
        if val > 0:
            return True
    return False
print(allPositive([-1,0,1]))