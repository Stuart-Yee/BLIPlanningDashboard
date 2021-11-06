"""
Implement the "wrap" function below.  It should accept a function as input and return a different function.  The newly created function should invoke the original input function on its parameters, and then either:

(a) Return the original function's return value if no exception is thrown.
- OR -
(b) Return the int 1000 if an exception was thrown during the invocation of the original function

Please see the `assert` tests below for clarification.
"""


def wrap(function):
    def inner(*args, **kwargs):
        try:
            function(*args, **kwargs)
            return function(*args, **kwargs)
        except:
            return 1000
    return inner

def function0(a):
    return 10


def function1(a, b, c):
    raise Exception("function1 exception")


def function2(a, b, c=10):
    return c


def function3(a=100, b=10, c="asdf"):
    if b < 10:
        raise Exception("function3 exception")
    return c


def function4():
    return "dog"


def function5(*args, **kwargs):
    if args[2] == 3 and kwargs["g"] == "house":
        return 0
    raise Exception("function5 exception")


function0 = wrap(function0)
function1 = wrap(function1)
function2 = wrap(function2)
function3 = wrap(function3)
function4 = wrap(function4)
function5 = wrap(function5)

assert (10 == function0(100))
assert (1000 == function0("a", "bc", 5))
assert (1000 == function1(0, 1, 2))
assert (30 == function2(0, 0, c=30))
assert (1000 == function2(0, 0, 0, c=30))
assert (1000 == function3(b=9))
assert ("asdf" == function3(b=10))
assert ("dog" == function4())
assert (1000 == function4(0))
assert (0 == function5(0, 0, 3, a=10, g="house"))
assert (1000 == function5())

print("Success — end of script reached!")