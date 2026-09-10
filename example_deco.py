from src.decorators import log

# @log(filename="mylog.txt")


@log("mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


my_function(2, "1")
