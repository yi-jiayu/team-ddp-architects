from heapq import heappush, heappop

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

a = [4, 65, 2, -31, 0, 99, 83, 782, 1]
# print(quickSort(a))
print(heapsort(a))