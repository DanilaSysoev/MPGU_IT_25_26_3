from copy import deepcopy

l1 = [1, 2, 3]
l2 = l1.copy()

print(id(l1))
print(id(l2))

l2[0] = 10
print(l1)
print(l2)

l3 = [[1], [2], [3]]
l4 = l3.copy()
l4[0] = 10
print(l3)
print(l4)

l3[1].append(10)
print(l3)
print(l4)

l3 = [[1], [2], [3]]
l4 = deepcopy(l3)
l4[0] = 10
print(l3)
print(l4)

l3[1].append(10)
print(l3)
print(l4)
