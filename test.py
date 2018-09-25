def outer():
    xn = "old hello!"

    def inner():
        # nonlocal xn
        xn = "new hello"

    inner()
    print(xn)


# outer()
num = 1
num2 = 3


def num_add(num):
    global num2
    num2 += 2
    num += 1


num_add(num)
print("out of main")

if __name__ == '__main__':
    num_add(num2)
    print(num2)
