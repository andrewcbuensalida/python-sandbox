def example(arg1, arg2, arg3="default3"):
    print(arg1, arg2, arg3)

args = {"arg2": "b"}
ex = example("a",'100',**args)
