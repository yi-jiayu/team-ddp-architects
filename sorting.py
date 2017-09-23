from heapq import heappush, heappop
import math
from random import randint

def count_sort(array):
    maximum = max(array)
    minimum = min(array)
    count_array = [0]*(maximum-minimum+1)

    for val in array:
        count_array[val-minimum] += 1

    sorted_array = []
    for i in range(minimum, maximum+1):
        if count_array[i-minimum] > 0:
            for j in range(0, count_array[i-minimum]):
                sorted_array.append(i)

    return sorted_array

# array = [3,2,-1,1,5,0,10,18,25,25]
# print array
# count_sort(array)

def heapsort(iterable):
     h = []
     for value in iterable:
         heappush(h, value)
     return [heappop(h) for i in range(len(h))]
     
def quickSort(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
        less = quickSort(less)
        more = quickSort(more)
        return less + pivotList + more

def qsort(inlist):
    if inlist == []: 
        return []
    else:
        pivot = inlist[0]
        lesser = qsort([x for x in inlist[1:] if x < pivot])
        greater = qsort([x for x in inlist[1:] if x >= pivot])
        return lesser + [pivot] + greater
a = [4, 65, 2, -31, 0, 99, 83, 782, 1]
# print(quickSort(a))
# print(heapsort(a))
print(count_sort(a))