
rag_chain = (
    {"name": "R"} | {"name": "A"} | {"name": "G"} | {"name": "C"} 
) # works without the parentheses as well
print(type(rag_chain))
print(rag_chain)

rag_chain2 = set([1,2,3]) | set([3,4,5,6]) 
print(rag_chain2)

rag_chain3 = 1 | 123 # the | symbol represents the bitwise OR operation. It performs a bitwise OR between the binary representations of the two operands.
# The number 1 is represented in binary as 0001.
# The number 123 is represented in binary as 1111011.
# When we perform the bitwise OR operation between these two binary numbers, we get 1111011, which is equivalent to the decimal number 123.
print(rag_chain3)

def test_func():
    return {"name": "Hello, World!", "age": 25}

def test_func2():
    return {"name": "Hello, World!2"}

rag_chain4 = test_func() | test_func2()
print(rag_chain4)