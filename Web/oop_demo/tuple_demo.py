t1 = ()
print(t1)

t2 = (1, 2, 3)
print(t2)

t3 = (1,)
print(t3)
print(type(t3))

t4 = ([1], [2], [3])
print(t4)
print(id(t4[0]), id(t4[1]), id(t4[2]))
t4[0].append(4)
t4[1].append(5)
t4[2].append(6)
print(t4)
print(id(t4[0]), id(t4[1]), id(t4[2]))
