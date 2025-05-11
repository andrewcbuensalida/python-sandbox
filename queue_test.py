from queue import Queue

q = Queue()

q.put('a')
q.put('b')

while not q.empty():
    print(q.get())