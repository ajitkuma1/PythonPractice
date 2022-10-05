def square(x):
    return x * x


def my_map(func, arg_list):
    returnList = []
    for i in arg_list:
        returnList.append(func(i))
    return returnList

def cube(x):
    return x * x * x

func = cube 
print(my_map(func, [2,10,4,6,8]))