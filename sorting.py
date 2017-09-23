from heapq import heappush, heappop
import math
from random import randint
import numpy as np

from heapq import merge
  
def merge_sort(m):
    if len(m) <= 1:
        return m
  
    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]
  
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))

def numpyy(arr):
    return np.sort(arr)

def np_count_sort(a):
    buckets = np.bincount(a)
    return np.repeat(np.arange(buckets.shape()[0] + 1), buckets)

def ins_sort(k):
    for i in range(1,len(k)):    #since we want to swap an item with previous one, we start from 1
        j = i                    #bcoz reducing i directly will mess our for loop, so we reduce its copy j instead
        temp = k[j]              #temp will be used for comparison with previous items, and sent to the place it belongs
        while j > 0 and temp < k[j-1]: #j>0 bcoz no point going till k[0] since there is no seat available on its left, for temp
            k[j] = k[j-1] #Move the bigger item 1 step right to make room for temp
            j=j-1 #take k[j] all the way left to the place where it has a smaller/no value to its left.
        k[j] = temp
    return k

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
# print(merge_sort(a))