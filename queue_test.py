from queue import Queue

q = Queue(maxsize=2)

q.put('a')
q.put('b')
# q.put('c') # this will hang 

while not q.empty():
    print(q.get())

# q.get() # will hang