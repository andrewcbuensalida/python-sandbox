# Problem Statement: Design a MinStack class that supports pushing, popping,
# retrieving the top element, and retrieving the minimum element in constant time O(1).
# Requirements:
# 1. push(x): Pushes element x onto the stack.
# 2. pop(): Removes the element on top of the stack.
# 3. top(): Gets the top element of the stack.
# 4. getMin(): Retrieves the minimum element in the stack.
# 5. The MinStack should be efficient in terms of space and time, ensuring all
# operations are performed in O(1) time complexity.

# Constraints:
#  Assume all operations are valid (e.g., a pop or top operation will only be called if
# there is at least one element in the stack).
#  All stack operations (push, pop, top, getMin) should operate in O(1) time.
# Example Operations and Results:
# minStack = MinStack()
# minStack.push(-2)
# minStack.push(0)
# minStack.push(-3)
# minStack.getMin() // Returns -3.
# minStack.pop()
# minStack.top() // Returns 0.
# minStack.getMin() // Returns -2.

# [-2]
# [-2, 0]
# [-2, 0, -3]
# getMin = -3
# [-2, 0]
# top = 0
# getMin = -2

# list version
# class MinStack:
#     stack = []
#     def push(self,element):
#         print('pushing')
#         self.stack.append(element)
#         print(self.stack)

#     def getMin(self):
#         print('sorting')
#         copy_stack = self.stack.copy()
#         copy_stack.sort()
#         print('''*Example copy_stack:\n''', copy_stack)
#         return copy_stack[0]
    
#     def pop(self):
#         self.stack.pop()
#         print(self.stack)

#     def top(self):
#         return self.stack[-1]
    
# linked list version
class Node:
    def __init__(self, value, min_value):
        self.value = value
        self.min_value = min_value
        self.next = None

class MinStack:
    def __init__(self):
        self.head = None

    def push(self, x: int) -> None:
        if not self.head:
            self.head = Node(x, x)
        else:
            new_node = Node(x, min(x, self.head.min_value))
            new_node.next = self.head
            self.head = new_node

    def pop(self) -> None:
        if self.head:
            self.head = self.head.next

    def top(self) -> int:
        if self.head:
            return self.head.value
        return None

    def getMin(self) -> int:
        if self.head:
            return self.head.min_value
        return None


minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
print(minStack.getMin()) # Returns -3.
minStack.pop()
print(minStack.top()) # Returns 0.
print(minStack.getMin()) # Returns -2.