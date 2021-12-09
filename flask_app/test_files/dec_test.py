





def my_decorator(a_function):
    def inner(*args, **kwargs):
        if kwargs.get('color') == "Red":
            print("oh my favorite color!")
        else:
            print("here's a boring color:")
        return a_function(*args, **kwargs)
    return inner

@my_decorator
def print_color(color):
    print(color)

print_color(color="Red")

print_color(color="Blue")

